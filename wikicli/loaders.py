"""Read original sources from vault/raw/ into located text sections.

Every section keeps a human-readable locator (a PDF page, an EPUB chapter, or a
Markdown heading) so passages and citations can point back to the exact spot in
the unchanged original. Nothing here writes to the source files.
"""

from __future__ import annotations

import hashlib
import html
import re
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from posixpath import dirname, join, normpath

SUPPORTED = {".pdf", ".epub", ".md", ".txt"}


@dataclass
class Section:
    source: str  # path relative to the vault, e.g. "raw/VC Math #1.pdf"
    locator: str  # "p. 6", "ch. 4: Carried Interest", "## Heading"
    text: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def clean(text: str) -> str:
    text = text.replace(" ", " ").replace("­", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


# --- PDF -------------------------------------------------------------------

# Browser "print to PDF" adds a date/title/URL header and a page counter to
# every page. They are not part of the article, so drop them from passages.
_PRINT_ARTIFACTS = [
    re.compile(r"^\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2} .*$", re.M),
    re.compile(r"^https?://\S+\s+\d+/\d+$", re.M),
]


def load_pdf(path: Path, rel: str, exclude_pages=(), strip_patterns=()) -> list[Section]:
    from pypdf import PdfReader

    patterns = _PRINT_ARTIFACTS + [re.compile(p, re.M) for p in strip_patterns]
    sections = []
    for i, page in enumerate(PdfReader(path).pages, start=1):
        if i in exclude_pages:
            continue
        text = page.extract_text() or ""
        for pattern in patterns:
            text = pattern.sub("", text)
        text = clean(text)
        if len(text) >= 40:  # skip image-only slides; nothing to cite
            sections.append(Section(rel, f"p. {i}", text))
    return sections


# --- EPUB ------------------------------------------------------------------


class _XHTMLText(HTMLParser):
    """Turn one EPUB chapter into (heading, text) blocks.

    Calibre-converted books mark sub-headings as <h1>-<h3> or as paragraphs
    whose class starts with "headline"/"chaptit"; both start a new block.
    """

    BLOCKS = {"p", "div", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[list[str]] = [["", ""]]  # [heading, text]
        self._heading_depth = 0
        self._stack: list[bool] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self._skip += 1
        cls = dict(attrs).get("class") or ""
        is_heading = tag in ("h1", "h2", "h3") or (tag == "p" and cls.startswith(("headline", "chaptit")))
        if tag in ("h1", "h2", "h3", "p"):
            self._stack.append(is_heading)
            if is_heading:
                if self._heading_depth == 0:
                    self.blocks.append(["", ""])
                self._heading_depth += 1
        if tag in self.BLOCKS:
            self.blocks[-1][1] += "\n"

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip -= 1
        if tag in ("h1", "h2", "h3", "p") and self._stack and self._stack.pop():
            self._heading_depth -= 1
        if tag in self.BLOCKS:
            self.blocks[-1][1] += "\n"

    def handle_data(self, data):
        if self._skip:
            return
        if self._heading_depth:
            self.blocks[-1][0] += data
        else:
            self.blocks[-1][1] += data


def _spine(z: zipfile.ZipFile) -> list[str]:
    container = z.read("META-INF/container.xml").decode()
    opf_path = re.search(r'full-path="([^"]+)"', container).group(1)
    opf = z.read(opf_path).decode()
    base = dirname(opf_path)
    manifest = {}  # id -> href, whatever order the attributes appear in
    for item in re.findall(r"<item\b[^>]*>", opf):
        item_id = re.search(r'\bid="([^"]+)"', item)
        href = re.search(r'\bhref="([^"]+)"', item)
        if item_id and href:
            manifest[item_id.group(1)] = href.group(1)
    order = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf)
    return [normpath(join(base, html.unescape(manifest[i]))) for i in order if i in manifest]


# Book front/back matter that only repeats keywords (and would outrank real
# content in keyword search) or contains no subject matter.
_EPUB_SKIP = re.compile(
    r"^(table of contents|contents|acknowledg|endnotes|about me|about the author)|copyright ©",
    re.I,
)


def load_epub(path: Path, rel: str) -> list[Section]:
    sections = []
    with zipfile.ZipFile(path) as z:
        for n, name in enumerate(_spine(z), start=1):
            parser = _XHTMLText()
            parser.feed(z.read(name).decode("utf-8", errors="replace"))
            full = clean("".join(h + "\n" + t for h, t in parser.blocks))
            if len(full) < 300 or _EPUB_SKIP.search(full[:400]):
                continue
            # Chapter title: the first heading, else the first short line.
            first_line = full.split("\n", 1)[0].strip()
            chapter = next((clean(h) for h, _ in parser.blocks if clean(h)), "") or first_line[:70]
            if chapter.lower().startswith("chapter") is False and len(first_line) < 70:
                chapter = first_line  # e.g. case-study chapters titled by a person's name
            for heading, text in parser.blocks:
                heading, text = clean(heading), clean(text)
                if len(text) < 40:
                    continue
                locator = chapter if not heading or heading == chapter else f"{chapter} › {heading}"
                sections.append(Section(rel, locator, text))
    return sections


# --- Markdown / text -------------------------------------------------------


def load_markdown(path: Path, rel: str) -> list[Section]:
    text = path.read_text(encoding="utf-8", errors="replace")
    sections, heading, buf = [], "top", []
    for line in text.splitlines():
        if re.match(r"^#{1,3} ", line):
            if "".join(buf).strip():
                sections.append(Section(rel, heading, clean("\n".join(buf))))
            heading, buf = line.lstrip("#").strip(), []
        else:
            buf.append(line)
    if "".join(buf).strip():
        sections.append(Section(rel, heading, clean("\n".join(buf))))
    return sections


def load_source(path: Path, rel: str, exclude_pages=(), strip_patterns=()) -> list[Section]:
    """Extract located sections. `exclude_pages`/`strip_patterns` come from sources.yml."""
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path, rel, exclude_pages, strip_patterns)
    if suffix == ".epub":
        return load_epub(path, rel)
    if suffix in (".md", ".txt"):
        return load_markdown(path, rel)
    raise ValueError(f"Unsupported source type {suffix!r} for {path.name} (supported: {sorted(SUPPORTED)})")
