"""`wiki verify`: audit every wiki note against the original sources it cites.

For each note:
- every footnote must resolve to at least one indexed passage of the original source
  (a PDF page range, or a book chapter/section locator);
- every number in a footnoted line must appear in the passages that line cites.
Lines marked "(my arithmetic)" are the reviewer's own calculations and are reported as such
rather than checked. No model is involved.
"""

from __future__ import annotations

import re

from .citations import _numbers, _trivial, passage_values, supported
from .ingest import existing_notes, rel_vault
from .retrieval import Passage, load_index

_FOOTNOTE_DEF = re.compile(r"^\[\^(\d+)\]: .*?\[\[(raw/[^\]|#]+)(?:#page=\d+)?\|([^\]]+)\]\]", re.M)
_PAGES = re.compile(r"pp?\. (\d+)(?:–(\d+))?")


def _pages(locator: str) -> set[int]:
    m = _PAGES.fullmatch(locator)
    if not m:
        return set()
    first = int(m.group(1))
    return set(range(first, int(m.group(2) or first) + 1))


def passages_for(file: str, label: str, passages: list[Passage]) -> list[Passage]:
    """Passages of `file` that a footnote label such as "pp. 48–50" or "Chapter 2 › How Does It Work?" points to."""
    same_file = [p for p in passages if p.source_file == file]
    wanted_pages = _pages(label)
    if wanted_pages:
        return [p for p in same_file if _pages(p.locator) & wanted_pages]
    exact = [p for p in same_file if p.locator == label]
    if exact:
        return exact
    tail = label.split(" › ")[-1]
    return [p for p in same_file if label in p.locator or p.locator in label or p.locator.endswith(tail)]


def audit_note(body: str, passages: list[Passage]) -> dict:
    main, _, sources = body.partition("\n## Sources\n")
    targets = {}
    unresolved = []
    for num, file, label in _FOOTNOTE_DEF.findall(sources):
        found = passages_for(file, label, passages)
        targets[num] = found
        if not found:
            unresolved.append(f"[^{num}] {file} · {label}")
    checked, own_math, problems = 0, 0, []
    body_start = main.find("\n## ")  # skip the title and the description/topic header
    related = main.find("\n## Related notes")
    for line in main[body_start:related if related > 0 else None].splitlines():
        refs = re.findall(r"\[\^(\d+)\]", line)
        if not refs:
            if line.startswith("> [!question]"):
                continue  # a practice question states the problem; its answer line carries the citation
            if any(not _trivial(v) for v in _numbers(line)) and "my arithmetic" not in line:
                problems.append(f"numbers without any citation: “{line.strip()[:110]}”")
            continue
        if "my arithmetic" in line:
            own_math += 1
            continue
        text = re.sub(r"\[\^\d+\]", "", line)
        claimed = _numbers(text)
        available: set[str] = set()
        for r in refs:
            for p in targets.get(r, []):
                available |= passage_values(p.text + " " + p.locator)
        for value, written in claimed.items():
            if _trivial(value):
                continue
            checked += 1
            if not supported(value, available):
                problems.append(f"{written} not in cited {', '.join('[^' + r + ']' for r in refs)}: “{text.strip()[:110]}”")
    return {"footnotes": len(targets), "unresolved": unresolved, "numbers": checked, "own_math_lines": own_math, "problems": problems}


def run() -> int:
    passages = load_index("raw").passages
    notes = existing_notes()
    totals = {"notes": 0, "footnotes": 0, "numbers": 0, "unresolved": 0, "problems": 0}
    print("wiki verify · every footnote resolves to source passages; every number appears in the passage it cites\n")
    for wid, note in sorted(notes.items(), key=lambda kv: rel_vault(kv[1].path)):
        if note.meta.get("type") != "concept":
            continue
        r = audit_note(note.body, passages)
        totals["notes"] += 1
        for k in ("footnotes", "numbers"):
            totals[k] += r[k]
        totals["unresolved"] += len(r["unresolved"])
        totals["problems"] += len(r["problems"])
        flag = "OK " if not (r["unresolved"] or r["problems"]) else "FIX"
        extra = f" · {r['own_math_lines']} line(s) of marked own arithmetic" if r["own_math_lines"] else ""
        print(f"{flag} {rel_vault(note.path):58} {r['footnotes']:2} footnotes · {r['numbers']:3} numbers checked{extra}")
        for u in r["unresolved"]:
            print(f"      unresolved footnote: {u}")
        for p in r["problems"]:
            print(f"      {p}")
    print(f"\n{totals['notes']} notes · {totals['footnotes']} footnotes ({totals['unresolved']} unresolved) · "
          f"{totals['numbers']} numbers checked ({totals['problems']} not found in the cited passage)")
    return 1 if totals["unresolved"] or totals["problems"] else 0
