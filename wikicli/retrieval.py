"""The retrieval tool: passages, a local BM25 keyword index, and search.

This module never imports the language model, so `wiki search` works even when
Gemma is unavailable. Passages live in data/index/ (outside the Obsidian vault):

    data/index/raw/<source-id>.jsonl   passages from the original sources (evidence)
    data/index/wiki.jsonl              passages from generated wiki notes (navigation only)

Ask mode searches only the raw passages, so generated text is never used as evidence.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from functools import cache

from .config import INDEX_DIR, WikiError
from .loaders import Section


@dataclass
class Passage:
    id: str  # "<source-id>:<n>", a machine ID used only inside data/
    source_id: str
    source_file: str  # vault-relative, e.g. "raw/Harlem Capital - Return the Fund.pdf"
    source_note: str  # readable wiki note for the source
    locator: str  # "p. 3" or "Chapter 2: Early Stage Investing › How Does It Work?"
    text: str
    kind: str = "raw"  # "raw" (original evidence) or "wiki" (generated note)

    @property
    def label(self) -> str:
        return f"{self.source_note}, {self.locator}"


@dataclass
class Hit:
    passage: Passage
    score: float
    coverage: float  # share of the query's IDF weight present in the passage (0-1)
    matched: list[str] = field(default_factory=list)


# --- Chunking ----------------------------------------------------------------

_SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9“\"$(])")


def _words(text: str) -> int:
    return len(text.split())


def chunk_section(section: Section, target: int, overlap: int) -> list[str]:
    """Split one located section into passages of ~`target` words.

    Paragraph boundaries are kept where possible. A long paragraph is split at
    sentence boundaries. Each new passage repeats the last ~`overlap` words of
    the previous one (whole sentences) so a fact on a boundary is not lost.
    A PDF page shorter than 1.6 x target stays whole, since slides read as a unit.
    """
    text = section.text
    if _words(text) <= target * 1.6:
        return [text]
    units: list[str] = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if _words(para) > target:
            units.extend(s.strip() for s in _SENTENCE.split(para) if s.strip())
        else:
            units.append(para)

    chunks, current = [], []
    for unit in units:
        if current and _words(" ".join(current)) + _words(unit) > target:
            chunks.append("\n\n".join(current))
            tail, n = [], 0
            for prev in reversed(_SENTENCE.split(current[-1])):
                if n + _words(prev) > overlap:
                    break
                tail.insert(0, prev)
                n += _words(prev)
            current = [" ".join(tail)] if tail else []
        current.append(unit)
    if current:
        last = "\n\n".join(current)
        if chunks and _words(last) < target * 0.25:  # fold a tiny remainder into the previous passage
            chunks[-1] += "\n\n" + last
        else:
            chunks.append(last)
    return chunks


def _group_key(section: Section) -> str:
    """Sections that may be merged share a key: the same PDF, or the same book chapter."""
    return section.source + "|" + (section.locator.split(" › ")[0] if not section.locator.startswith("p. ") else "")


def _merged_locator(first: str, last: str) -> str:
    if first == last:
        return first
    if first.startswith("p. ") and last.startswith("p. "):
        return f"pp. {first[3:]}–{last[3:]}"
    chapter = first.split(" › ")[0]
    tail = last.split(" › ")[-1]
    return f"{first} … {tail}" if tail != chapter else first


def merge_short_sections(sections: list[Section], target: int) -> list[Section]:
    """Merge runs of short neighbouring sections (slides, small book subsections).

    A single slide often carries no topic words ("Post money … $14.6m") because the
    title is on the previous slide; merging neighbours keeps that context together.
    """
    merged: list[Section] = []
    run: list[Section] = []

    def flush() -> None:
        if run:
            text = "\n\n".join(
                (f"[{s.locator.split(' › ')[-1]}]\n" if len(run) > 1 and not s.locator.startswith("p. ") else "") + s.text
                for s in run
            )
            merged.append(Section(run[0].source, _merged_locator(run[0].locator, run[-1].locator), text))
            run.clear()

    for section in sections:
        size = _words(section.text)
        if run and (
            _group_key(run[-1]) != _group_key(section)
            or sum(_words(s.text) for s in run) + size > target
            or size > target * 0.6
        ):
            flush()
        run.append(section)
        if size > target * 0.6:
            flush()
    flush()
    return merged


def make_passages(sections: list[Section], source_id: str, source_note: str, target: int, overlap: int) -> list[Passage]:
    passages = []
    for section in merge_short_sections(sections, target):
        for text in chunk_section(section, target, overlap):
            passages.append(
                Passage(
                    id=f"{source_id}:{len(passages) + 1:03d}",
                    source_id=source_id,
                    source_file=section.source,
                    source_note=source_note,
                    locator=section.locator,
                    text=text,
                )
            )
    return passages


# --- Tokenising --------------------------------------------------------------

STOPWORDS = set(
    """a an and are as at be been but by can could did do does for from had has have how i if in into is it its
    me my of on or our so than that the their them then there these they this to was we were what when where
    which who whom why will with would you your about also any just more most much not only other some such
    very use using used give tell explain according notes note sources source wiki get got s""".split()
)

# Money shorthand in the sources is inconsistent ($40mm, $14.6m, 40 million, $4.3bn).
# Normalise so "40 million" and "$40mm" produce the same token "40m".
_MONEY = [
    (re.compile(r"(\d(?:[\d,]*\d)?(?:\.\d+)?)\s*(?:mm|mn|million|m)\b", re.I), r"\1m"),
    (re.compile(r"(\d(?:[\d,]*\d)?(?:\.\d+)?)\s*(?:bn|billion|b)\b", re.I), r"\1b"),
    (re.compile(r"(\d(?:[\d,]*\d)?(?:\.\d+)?)\s*(?:k|thousand)\b", re.I), r"\1k"),
    (re.compile(r"(\d)\s*percent\b", re.I), r"\1%"),
    # "pre-money", "pre money", "premoney" (and post-) are the same term
    (re.compile(r"\b(pre|post)[- ]?money\b", re.I), r"\1money"),
    (re.compile(r"'s\b"), ""),
]

# Small, explicit query-side synonym list for VC jargon. Expansions get half weight.
SYNONYMS = {
    "irr": ["internal", "rate", "return"],
    "lp": ["limited", "partner"],
    "lps": ["limited", "partner"],
    "gp": ["general", "partner"],
    "gps": ["general", "partner"],
    "carry": ["carried", "interest"],
    "vc": ["venture", "capital"],
    "vcs": ["venture", "capitalist"],
    "paid": ["fee", "salary", "profit", "carried", "interest"],
    "pay": ["fee", "salary", "profit"],
    "cac": ["customer", "acquisition", "cost"],
    "clv": ["customer", "lifetime", "value"],
    "ltv": ["customer", "lifetime", "value"],
    "mrr": ["monthly", "recurring", "revenue"],
    "arr": ["annualized", "run", "rate"],
}


def _stem(token: str) -> str:
    """Very light suffix stripping so 'returns'/'return', 'diluted'/'dilution' meet."""
    if token[0].isdigit() or len(token) <= 3:
        return token
    if token.endswith("ies") and len(token) > 4:
        return token[:-3] + "y"
    if token.endswith("s") and not token.endswith(("ss", "us", "is")):
        return token[:-1]
    for suffix in ("ing", "ed"):
        if token.endswith(suffix) and len(token) - len(suffix) >= 4:
            return token[: -len(suffix)]
    return token


def tokenize(text: str) -> list[str]:
    text = text.lower().replace("’", "'")
    for pattern, repl in _MONEY:
        text = pattern.sub(repl, text)
    text = text.replace(",", "")
    tokens = re.findall(r"[a-z0-9]+(?:[.\-][a-z0-9]+)*%?|\d+(?:\.\d+)?x", text)
    return [_stem(t) for t in tokens if t not in STOPWORDS]


# ... and the reverse direction: spelled-out phrases also match their acronyms.
PHRASES = {
    "venture capital": "vc",
    "limited partner": "lp",
    "general partner": "gp",
    "internal rate of return": "irr",
    "carried interest": "carry",
}


def query_terms(query: str) -> dict[str, float]:
    """Query tokens with weights: 1.0 for typed words, 0.5 for synonym expansions."""
    weights: dict[str, float] = {}
    lowered = query.lower()
    for raw in re.findall(r"[a-z0-9\-]+", lowered):
        for syn in SYNONYMS.get(raw, []):
            for t in tokenize(syn):
                weights.setdefault(t, 0.5)
    for phrase, acronym in PHRASES.items():
        if phrase in lowered:
            weights.setdefault(acronym, 0.5)
    for t in tokenize(query):
        weights[t] = 1.0
    return weights


# --- BM25 --------------------------------------------------------------------


class BM25:
    """Okapi BM25 over passage text plus its locator (so headings are searchable)."""

    def __init__(self, passages: list[Passage], k1: float = 1.5, b: float = 0.75):
        self.passages = passages
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(p.locator + "\n" + p.text)) for p in passages]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg_len = sum(self.lengths) / max(len(self.lengths), 1)
        self.df = Counter(t for d in self.docs for t in d)
        self.n = len(passages)

    def idf(self, term: str) -> float:
        df = self.df.get(term, 0)
        return math.log((self.n - df + 0.5) / (df + 0.5) + 1)

    def unknown_terms(self, query: str) -> list[str]:
        """Words the user typed that occur in no passage at all (e.g. "hurdle"). A hyphenated word
        counts as known when each of its parts is known ("five-year" vs "5-year" is still known)."""
        out = []
        for term, weight in query_terms(query).items():
            if weight < 1.0 or self.df.get(term, 0):
                continue
            parts = [_stem(p) for p in term.split("-") if p and p not in STOPWORDS]
            if "-" in term and parts and all(self.df.get(p, 0) or p in ("five", "one", "two", "three", "four") for p in parts):
                continue
            out.append(term)
        return out

    def search(self, query: str, k: int = 5, min_coverage: float = 0.0, dedupe: float = 0.8) -> list[Hit]:
        weights = query_terms(query)
        if not weights:
            return []
        total_idf = sum(self.idf(t) * w for t, w in weights.items())
        scored = []
        for i, doc in enumerate(self.docs):
            score, covered, matched = 0.0, 0.0, []
            norm = self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg_len)
            for term, w in weights.items():
                tf = doc.get(term)
                if not tf:
                    continue
                idf = self.idf(term)
                score += w * idf * tf * (self.k1 + 1) / (tf + norm)
                covered += w * idf
                matched.append(term)
            if score > 0:
                scored.append((score, i, Hit(self.passages[i], score, covered / total_idf, matched)))
        scored.sort(key=lambda x: x[0], reverse=True)

        # Slides repeat the same table on several pages; keep only one copy.
        hits: list[Hit] = []
        kept: list[set] = []
        for _, i, hit in scored:
            if hit.coverage < min_coverage:
                continue
            tokens = set(self.docs[i])
            if any(_jaccard(tokens, other) > dedupe for other in kept):
                continue
            hits.append(hit)
            kept.append(tokens)
            if len(hits) == k:
                break
        return hits


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / max(len(a | b), 1)


# --- Persistence ---------------------------------------------------------------


def save_passages(path, passages: list[Passage]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for p in passages:
            f.write(json.dumps(asdict(p), ensure_ascii=False) + "\n")


def _read(path) -> list[Passage]:
    return [Passage(**json.loads(line)) for line in path.read_text().splitlines() if line.strip()]


@cache
def load_index(scope: str = "raw") -> BM25:
    """scope: "raw" (original evidence), "wiki" (generated notes), or "all"."""
    files = []
    if scope in ("raw", "all"):
        files += sorted((INDEX_DIR / "raw").glob("*.jsonl"))
    if scope in ("wiki", "all") and (INDEX_DIR / "wiki.jsonl").exists():
        files.append(INDEX_DIR / "wiki.jsonl")
    passages = [p for f in files for p in _read(f)]
    if not passages:
        raise WikiError("The search index is empty. Run `wiki ingest vault/raw` first.")
    return BM25(passages)
