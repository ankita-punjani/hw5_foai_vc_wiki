"""`wiki ingest`: original sources -> passages -> Gemma-drafted wiki notes -> index.md.

Naming and de-duplication rules:
- Note filenames come from sources.yml (`note`) and instructions/topics.yml (`name`),
  never from the model, so names stay short and readable.
- Every note carries a stable `wiki_id` in its frontmatter. Ingest finds existing
  notes by that ID (even if you renamed the file in Obsidian) and updates them in
  place instead of creating a second copy.
- A note whose frontmatter says `status: reviewed` is never overwritten. If its
  evidence changed, or with --redraft, a fresh draft goes to data/drafts/ for comparison.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml

from . import runlog
from .config import DRAFTS, INDEX_DIR, INDEX_MD, RAW, VAULT, WIKI, Source, WikiError, settings, source_for, sources, topics
from .loaders import SUPPORTED, load_source, sha256
from .prompts import ingest_messages, source_overview_messages
from .retrieval import Hit, Passage, load_index, make_passages, save_passages

# --- Notes on disk -------------------------------------------------------------


@dataclass
class Note:
    path: Path
    meta: dict
    body: str


def read_note(path: Path) -> Note:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        return Note(path, {}, text)
    return Note(path, yaml.safe_load(m.group(1)) or {}, m.group(2))


def write_note(path: Path, meta: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=1000).strip()
    path.write_text(f"---\n{front}\n---\n{body.rstrip()}\n")


def existing_notes() -> dict[str, Note]:
    """All wiki notes keyed by their stable wiki_id."""
    notes = {}
    for path in sorted(WIKI.rglob("*.md")):
        note = read_note(path)
        wid = note.meta.get("wiki_id")
        if wid:
            if wid in notes:
                raise WikiError(f"Duplicate wiki_id {wid!r} in {notes[wid].path} and {path}; merge them first.")
            notes[wid] = note
    return notes


# --- Links back to the original evidence -----------------------------------------


def source_link(p: Passage) -> str:
    """Obsidian link that opens the original file (at the page, for PDFs)."""
    page = re.match(r"pp?\. (\d+)", p.locator)
    target = f"{p.source_file}#page={page.group(1)}" if page else p.source_file
    return f"[[{target}|{p.locator}]]"


def footnotes_for(body: str, hits: list[Hit]) -> tuple[str, list[str], list[int]]:
    """Turn the model's [S3] markers into Obsidian footnotes [^1] pointing at sources.

    Returns (body, footnote lines, passage numbers that were invalid)."""
    order: dict[str, int] = {}  # one footnote per source location, not per passage
    first_passage: dict[str, Passage] = {}
    invalid: list[int] = []

    def repl(m: re.Match) -> str:
        n = int(m.group(1))
        if not 1 <= n <= len(hits):
            invalid.append(n)
            return ""
        p = hits[n - 1].passage
        key = f"{p.source_file}|{p.locator}"
        first_passage.setdefault(key, p)
        order.setdefault(key, len(order) + 1)
        return f"[^{order[key]}]"

    # The model sometimes writes [S5, S8] or [S5,8]; split into [S5][S8] first.
    body = re.sub(r"\[S(\d+(?:\s*,\s*S?\d+)+)\]", lambda m: "".join(f"[S{n}]" for n in re.findall(r"\d+", m.group(1))), body)
    body = re.sub(r"\[S(\d+)\]", repl, body)
    body = re.sub(r"(\[\^\d+\])\1+", r"\1", body)  # [^1][^1] -> [^1]
    lines = []
    for key, fn in sorted(order.items(), key=lambda kv: kv[1]):
        p = first_passage[key]
        lines.append(f"[^{fn}]: [[{p.source_note}]] · {source_link(p)} · `{p.source_file}`")
    return body, lines, invalid


def clean_model_body(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", text)
    text = re.sub(r"^# .*\n+", "", text)  # the harness writes the title
    text = re.split(r"\n#+\s*(Sources|References|Related( notes)?)\s*\n", text, flags=re.I)[0]
    text = re.sub(r"^#{3,}\s*", "## ", text, flags=re.M)
    return text.strip()


# --- Ingest --------------------------------------------------------------------


def resolve_inputs(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths or [str(RAW)]:
        path = Path(raw).expanduser()
        if not path.exists():
            raise WikiError(f"No such file or folder: {raw}")
        if path.is_dir():
            # raw/README.md documents the folder; it is not a source.
            files += sorted(p for p in path.iterdir() if p.suffix.lower() in SUPPORTED and p.name != "README.md")
        else:
            files.append(path)
    for f in files:
        if f.resolve().parent != RAW.resolve():
            raise WikiError(f"{f} is not in vault/raw/. Copy originals into vault/raw/ (unchanged) and ingest them there.")
    if not files:
        raise WikiError(f"No supported sources ({', '.join(sorted(SUPPORTED))}) found in {', '.join(paths)}")
    return files


def index_source(src: Source) -> dict:
    cfg = settings()["retrieval"]
    sections = load_source(src.path, src.rel, src.exclude_pages, src.strip_patterns)
    passages = make_passages(sections, src.id, src.note, cfg["passage_words"], cfg["passage_overlap_words"])
    save_passages(INDEX_DIR / "raw" / f"{src.id}.jsonl", passages)
    meta = {
        "id": src.id,
        "file": src.rel,
        "sha256": sha256(src.path),
        "sections": len(sections),
        "passages": len(passages),
        "words": sum(len(p.text.split()) for p in passages),
        "indexed_at": datetime.now().isoformat(timespec="seconds"),
    }
    (INDEX_DIR / "raw" / f"{src.id}.meta.json").write_text(json.dumps(meta, indent=2))
    return meta


def evidence_hash(hits: list[Hit]) -> str:
    h = hashlib.sha256()
    for hit in hits:
        h.update(hit.passage.id.encode() + hit.passage.text.encode())
    return h.hexdigest()[:16]


def run(paths: list[str], force: bool = False, redraft: bool = False, no_llm: bool = False) -> None:
    files = resolve_inputs(paths)
    ingested = [source_for(f) for f in files]
    record: dict = {"env": runlog.environment(), "sources": [], "notes": [], "command": {"paths": paths, "force": force, "redraft": redraft, "no_llm": no_llm}}
    log: list[str] = []

    def say(line: str) -> None:
        print(line)
        log.append(line)

    # 1. Originals -> located passages (the retrieval index).
    with runlog.Timer() as t_index:
        for src in ingested:
            meta = index_source(src)
            record["sources"].append(meta)
            say(f"indexed  {src.rel}: {meta['sections']} sections -> {meta['passages']} passages ({meta['words']:,} words) sha256 {meta['sha256'][:12]}…")
    load_index.cache_clear()
    index = load_index("raw")
    say(f"index    {index.n} passages from {len(list((INDEX_DIR / 'raw').glob('*.jsonl')))} sources ({t_index.seconds:.1f}s)")

    from .llm import LocalGemma

    gemma = None if no_llm else LocalGemma()
    cfg = settings()
    notes = existing_notes()
    ingested_ids = {s.id for s in ingested}
    generations = []

    # 2. Topic notes, drafted by Gemma from the passages retrieval selects for each topic.
    for topic in topics()["topics"]:
        wid = f"topic:{topic['id']}"
        hits = index.search(topic["name"] + " " + topic["query"], k=cfg["retrieval"]["ingest_top_k"])
        existing = notes.get(wid)
        if existing and not force:
            # An existing note is only affected by the sources it actually cites.
            cited = set(existing.meta.get("sources") or [])
            if not cited & {s.rel for s in ingested}:
                continue
        elif not ({h.passage.source_id for h in hits} & ingested_ids):
            continue  # a new topic that draws on none of the sources being ingested
        ev_hash = evidence_hash(hits)
        note = notes.get(wid)
        path = note.path if note else WIKI / topic["folder"] / f"{topic['name']}.md"
        status = (note.meta.get("status") if note else None) or "draft"
        unchanged = note is not None and note.meta.get("evidence_hash") == ev_hash

        if status == "reviewed" and not redraft:
            if unchanged:
                say(f"kept     {rel_vault(path)} (reviewed, evidence unchanged)")
                record["notes"].append({"note": rel_vault(path), "action": "kept-reviewed"})
                continue
            if no_llm:
                say(f"STALE    {rel_vault(path)} (reviewed, but its evidence changed; run without --no-llm to redraft)")
                continue
        elif status != "reviewed" and unchanged and not force:
            say(f"kept     {rel_vault(path)} (draft, evidence unchanged)")
            record["notes"].append({"note": rel_vault(path), "action": "kept-draft"})
            continue
        if no_llm:
            say(f"skipped  {topic['name']} (--no-llm)")
            continue

        gen = gemma.generate(
            ingest_messages(topic["name"], topic["description"], hits),
            max_tokens=cfg["generation"]["ingest_max_tokens"],
            temperature=cfg["generation"]["ingest_temperature"],
        )
        generations.append(gen)
        body, footnotes, invalid = footnotes_for(clean_model_body(gen.text), hits)
        meta = {
            "wiki_id": wid,
            "type": "concept",
            "topic": topic["folder"],
            "status": "draft",
            "description": topic["description"],
            # only sources the note actually cites (not every retrieved passage)
            "sources": sorted({m for f in footnotes for m in re.findall(r"`(raw/[^`]+)`", f)}),
            "evidence_passages": [h.passage.id for h in hits],
            "evidence_hash": ev_hash,
            "generated_by": gemma.model_id,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "tags": ["vc/" + topic["folder"].lower().replace(" ", "-")],
        }
        text = render_topic(topic, body, footnotes)
        action = "created" if note is None else "updated"
        if status == "reviewed":
            # Never overwrite a reviewed note: park the new draft for a human to compare.
            path = DRAFTS / f"{topic['name']}.md"
            action = "redrafted -> data/drafts (reviewed note untouched)"
        write_note(path, meta, text)
        flag = f" · {len(invalid)} invalid citation(s) dropped" if invalid else ""
        say(f"{action:8} {rel_vault(path)} · {gen.summary()}{flag}")
        record["notes"].append({"note": rel_vault(path), "action": action, "generation": gen.__dict__, "invalid_citations": invalid})

    # 3. One note per source: catalog facts, overview, contents, and backlinks.
    notes = existing_notes()
    for src in sources().values():
        if src.id in ingested_ids or f"source:{src.id}" not in notes:
            gen = write_source_note(src, notes, gemma, redraft)
            if gen:
                generations.append(gen)
            say(f"source   {rel_vault(source_note_path(src, notes))}" + (f" · {gen.summary()}" if gen else ""))

    # 4. Human landing page + wiki-note index for navigation searches.
    notes = existing_notes()
    write_index_md(notes)
    say(f"index.md rebuilt: {sum(1 for n in notes.values() if n.meta.get('type') == 'concept')} topic notes, "
        f"{sum(1 for n in notes.values() if n.meta.get('type') == 'source')} source notes")
    save_passages(INDEX_DIR / "wiki.jsonl", wiki_passages(notes))
    load_index.cache_clear()

    if generations:
        total = sum(g.seconds for g in generations)
        peak = max(g.peak_memory_gb for g in generations)
        rss = max(g.process_rss_gb for g in generations)
        say(f"gemma    {len(generations)} generations in {total:.0f}s (+{gemma.load_seconds or 0:.1f}s load) · peak MLX memory {peak:.2f} GB · process max RSS {rss:.2f} GB")
    record["log"] = log
    out = runlog.write("ingest", "# wiki ingest\n\n```\n" + "\n".join(log) + "\n```\n", record)
    print(f"saved    {runlog.rel(out)}")


def rel_vault(path: Path) -> str:
    try:
        return str(path.relative_to(VAULT))
    except ValueError:
        return runlog.rel(path)


def render_topic(topic: dict, body: str, footnotes: list[str]) -> str:
    source_notes = sorted({re.search(r"\[\[([^\]|]+)\]\]", f).group(1) for f in footnotes})
    lines = [
        f"# {topic['name']}",
        "",
        f"> {topic['description']}",
        f"> Topic: [[index#{topic['folder']}|{topic['folder']}]] · From: " + (", ".join(f"[[{s}]]" for s in source_notes) or "—"),
        "",
        body.strip(),
        "",
        "## Related notes",
        *[f"- [[{r['to']}]] — {r['why']}" for r in topic.get("related", [])],
        "",
        "## Sources",
        "Each footnote opens the original file in `raw/` at the cited page or section.",
        "",
        *footnotes,
    ]
    return "\n".join(lines)


# --- Source notes ----------------------------------------------------------------


def source_note_path(src: Source, notes: dict[str, Note]) -> Path:
    note = notes.get(f"source:{src.id}")
    return note.path if note else WIKI / "Sources" / f"{src.note}.md"


def source_outline(src: Source) -> list[tuple[str, str]]:
    """(locator, first line) for each indexed section, in order, deduplicated."""
    path = INDEX_DIR / "raw" / f"{src.id}.jsonl"
    seen, out = set(), []
    for line in path.read_text().splitlines():
        p = json.loads(line)
        if p["locator"] in seen:
            continue
        seen.add(p["locator"])
        first = re.sub(r"\s+", " ", p["text"]).strip()[:110]
        out.append((p["locator"], first))
    return out


def write_source_note(src: Source, notes: dict[str, Note], gemma, redraft: bool):
    path = source_note_path(src, notes)
    existing = notes.get(f"source:{src.id}")
    meta_file = INDEX_DIR / "raw" / f"{src.id}.meta.json"
    index_meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
    outline = source_outline(src)

    overview, gen = None, None
    if existing and existing.meta.get("status") == "reviewed" and not redraft:
        m = re.search(r"## Overview\n(.*?)\n## ", existing.body, re.S)
        overview = m.group(1).strip() if m else None
    elif existing and not redraft and existing.meta.get("sha256") == index_meta.get("sha256"):
        m = re.search(r"## Overview\n(.*?)\n## ", existing.body, re.S)
        overview = m.group(1).strip() if m else None
    if overview and overview.startswith("_Overview not generated"):
        overview = None  # placeholder from an earlier --no-llm run
    if overview is None and gemma is not None:
        sample = "\n".join(f"- {loc}: {first}" for loc, first in outline[:70])
        gen = gemma.generate(source_overview_messages(src.title, sample), max_tokens=220, temperature=0.0)
        overview = gen.text.strip()
    overview = overview or "_Overview not generated yet (run `wiki ingest` without --no-llm)._"

    # Topic notes that cite this source (backlinks, computed not generated).
    citing = sorted(
        (n.path.stem, n.meta.get("topic", ""))
        for n in notes.values()
        if n.meta.get("type") == "concept" and src.rel in (n.meta.get("sources") or [])
    )
    # Contents: chapters for the book, page ranges for PDFs.
    if src.file.endswith(".epub"):
        chapters = list(dict.fromkeys(loc.split(" › ")[0] for loc, _ in outline))
        contents = [f"- {c}" for c in chapters]
    else:
        contents = [f"- [[{src.rel}#page={re.match(r'pp?\. (\d+)', loc).group(1)}|{loc}]] — {first[:80]}"
                    for loc, first in outline if re.match(r"pp?\. \d", loc)]

    meta = {
        "wiki_id": f"source:{src.id}",
        "type": "source",
        "status": existing.meta.get("status", "draft") if existing else "draft",
        "source_id": src.id,
        "title": src.title,
        "author": src.author,
        "published": src.published,
        "kind": src.kind,
        "url": src.url,
        "file": src.rel,
        "original_filename": src.original_filename,
        "sha256": index_meta.get("sha256", ""),
        "passages": index_meta.get("passages", 0),
        "tags": ["vc/source"],
    }
    body = "\n".join([
        f"# {src.note}",
        "",
        f"> Original file: [[{src.rel}]] (unchanged) · Catalog: [[index#Sources|index]]",
        "",
        "| | |",
        "|---|---|",
        f"| Title | {src.title} |",
        f"| Author | {src.author} |",
        f"| Published | {src.published} |",
        f"| Type | {src.kind} |",
        f"| Link | {src.url or '—'} |",
        f"| Original filename | `{src.original_filename}` |",
        f"| SHA-256 | `{index_meta.get('sha256', '')[:16]}…` |",
        f"| Indexed | {index_meta.get('sections', 0)} sections → {index_meta.get('passages', 0)} passages |",
        f"| Excluded | {('pages ' + ', '.join(map(str, src.exclude_pages)) + ' (site footer, not the article)') if src.exclude_pages else '—'} |",
        f"| Rights | {src.license_note} |",
        "",
        "## Overview",
        overview,
        "",
        "## Wiki notes built from this source",
        *([f"- [[{name}]] ({topic})" for name, topic in citing] or ["- none yet"]),
        "",
        "## Contents",
        *contents,
    ])
    if gen and existing and existing.meta.get("status") == "reviewed":
        write_note(DRAFTS / f"{src.note}.md", meta, body)
    else:
        write_note(path, meta, body)
    return gen


# --- index.md and wiki passages ---------------------------------------------------


def write_index_md(notes: dict[str, Note]) -> None:
    by_id = {n.meta["wiki_id"]: n for n in notes.values()}
    t = topics()
    lines = [
        "# VC Math Wiki",
        "",
        # One line per paragraph: Obsidian shows every source line break.
        "**A beginner's guide to venture capital:** how venture funds work, how investors get paid, the math "
        "behind \"return the fund\", dilution and valuation, and how to break into the industry. It is about VC "
        "in general, not any one firm. One source is a seed fund's public walk-through of its own math, used "
        "here as a worked example.",
        "",
        "Every note was drafted by a local Gemma model from three sources, then checked claim by claim. Each "
        "fact has a footnote that opens the original page or section in `raw/`, and each note links to "
        "related notes with a reason.",
        "",
        "**New to VC? Read in this order:** [[How Venture Capital Works]] → [[Venture Fund Structure]] → "
        "[[Management Fees and Carried Interest]] → [[Power Law of Venture Returns]] → [[Return the Fund]] → "
        "[[Pre-Money and Post-Money Valuation]] → [[Dilution]] → [[Venture Capital Method]] → [[Scenario Analysis]] → "
        "[[VC Math Practice Problems]]. Keep [[VC Glossary]] open for unfamiliar words.",
        "",
    ]
    for folder in t["folders"]:
        lines += [f"## {folder['name']}", f"_{folder['blurb']}_", ""]
        for topic in t["topics"]:
            if topic["folder"] != folder["name"]:
                continue
            note = by_id.get(f"topic:{topic['id']}")
            if not note:
                lines.append(f"- {topic['name']} — {topic['description']} _(not generated yet)_")
                continue
            draft = "" if note.meta.get("status") == "reviewed" else " _(draft)_"
            lines.append(f"- [[{note.path.stem}]] — {topic['description']}{draft}")
        lines.append("")
    lines += ["## Sources", "_The three originals, unchanged, with their catalog details. The wiki's scope is general VC; the "
              "seed-fund post is one fund's worked example._", ""]
    for src in sources().values():
        note = by_id.get(f"source:{src.id}")
        name = note.path.stem if note else src.note
        lines.append(f"- [[{name}]] — {src.kind}, {src.author} ({src.published}) · file: `{src.rel}`")
    lines += ["", "---", f"_Rebuilt by `wiki ingest` on {datetime.now():%Y-%m-%d %H:%M}. Draft notes are Gemma output not yet checked against the sources._", ""]
    INDEX_MD.write_text("\n".join(lines))


def wiki_passages(notes: dict[str, Note]) -> list[Passage]:
    out = []
    for note in notes.values():
        name = note.path.stem
        body = re.split(r"\n## Sources\n", note.body)[0]
        for block in re.split(r"\n(?=## )", body):
            heading = block.splitlines()[0].lstrip("# ").strip() if block.strip() else ""
            text = re.sub(r"\[\^\d+\]", "", block).strip()
            if len(text) < 40:
                continue
            out.append(Passage(
                id=f"{note.meta['wiki_id']}:{len(out) + 1:03d}",
                source_id=note.meta["wiki_id"],
                source_file=rel_vault(note.path),
                source_note=name,
                locator=heading if heading != name else "intro",
                text=text,
                kind="wiki",
            ))
    return out
