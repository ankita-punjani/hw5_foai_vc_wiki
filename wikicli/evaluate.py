"""`wiki eval`: run the pre-registered ask-mode tests and write evidence cards.

Each card records the question, the expected evidence (written before the run),
whether retrieval surfaced it, the exact Gemma answer, and the automatic citation
checks. The human assessment section is left for a person to fill in after
opening the cited sources — the harness does not grade its own answers.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import yaml

from .config import ROOT
from .modes import ask

CARDS = ROOT / "evidence" / "ask"


def _pages(text: str) -> set[int]:
    pages = set()
    for a, b in re.findall(r"(\d+)(?:\s*[-–]\s*(\d+))?", text):
        pages |= set(range(int(a), int(b or a) + 1))
    return pages


def _expected_found(expected: dict, hits: list[dict]) -> str:
    """Did a retrieved passage come from the expected file AND location?

    PDF locators are compared as page ranges ("pp. 48-50" matches "pp. 48–50" or "p. 49"); book
    locators by their section heading (the part after the last "›"). Alternatives are separated by " / "."""
    file = expected["file"]
    found = []
    for alt in expected["locator"].split(" / "):
        alt = alt.strip()
        for i, h in enumerate(hits, 1):
            if h["file"] != file:
                continue
            if re.match(r"pp?\.", alt):
                ok = bool(_pages(alt) & _pages(h["locator"])) if re.match(r"pp?\.", h["locator"]) else False
            else:
                heading = alt.split("›")[-1].strip()
                ok = heading.lower() in h["locator"].lower()
            if ok and f"[S{i}]" not in " ".join(found):
                found.append(f"[S{i}] {h['locator']}")
    if found:
        return "yes — " + "; ".join(found)
    same_file = [f"[S{i}] {h['locator']}" for i, h in enumerate(hits, 1) if h["file"] == file]
    return "NO (same source, other sections: " + ", ".join(same_file) + ")" if same_file else "NO"


def run(tests_path: str, only: list[str] | None) -> None:
    spec = yaml.safe_load(Path(tests_path).read_text())
    CARDS.mkdir(parents=True, exist_ok=True)
    for test in spec["tests"]:
        if only and test["id"] not in only:
            continue
        print(f"\n{'=' * 30} {test['id']} ({test['kind']}) {'=' * 30}")
        r = ask(test["question"], tag=f"eval-{test['id']}")
        hits = r["retrieval"]["hits"]
        exp_lines = []
        for e in test.get("expected_sources") or []:
            exp_lines += [f"- `{e['file']}` — {e['locator']}", f"  - expected passage: “{e['passage']}”",
                          f"  - retrieved? **{_expected_found(e, hits)}**"]
        if not exp_lines:
            exp_lines = ["- none: no source should answer this question"] + ([f"- trap: {test['trap']}"] if test.get("trap") else [])
        env, gen, cit = r["env"], r["generation"], r["citations"]
        card = "\n".join([
            f"# {test['id']}: {test['question']}",
            "",
            f"**Test type:** {test['kind']}  ",
            f"**Expected behavior (written before the run):** {test['expected_behavior']}",
            "",
            "| Run detail | Value |",
            "|---|---|",
            f"| Mode | ask (standalone; no chat history, no persona) |",
            f"| Execution | {r['execution']} |",
            f"| Network at run time | {env['network']} |",
            f"| Model | `{env['model']}` |",
            f"| Runtime | {env['runtime']} |",
            f"| Device | {env['device']} |",
            f"| Timestamp | {env['timestamp']} |",
            f"| Retrieval | BM25 top {r['retrieval']['top_k']} over original-source passages, {r['retrieval']['seconds'] * 1000:.0f} ms |",
            f"| Generation | {gen['seconds']:.1f}s, {gen['prompt_tokens']} prompt + {gen['generated_tokens']} generated tokens, {gen['tokens_per_second']:.0f} tok/s |",
            f"| Memory | peak MLX {gen['peak_memory_gb']:.2f} GB · process max RSS {gen['process_rss_gb']:.2f} GB |",
            f"| Full run log | [{Path(r['saved']).name}](../../outputs/runs/{Path(r['saved']).name}) |",
            "",
            "## Expected evidence",
            "",
            *exp_lines,
            "",
            "Expected facts: " + ("; ".join(test.get("expected_answer_facts") or []) or "an explicit insufficient-evidence statement"),
            "",
            "## Retrieved passages",
            "",
            *[f"{i}. **[S{i}] {h['source_note']}, {h['locator']}** — `{h['file']}` (score {h['score']}, coverage {h['coverage']:.0%})" for i, h in enumerate(hits, 1)],
            "",
            "## Gemma answer (verbatim)",
            "",
            "\n".join("> " + line for line in r["answer"].splitlines()),
            "",
            "## Citation check (automatic)",
            "",
            f"- cited: {', '.join(f'[S{n}]' for n in cit['cited']) or 'none'}",
            f"- invalid citations: {', '.join(cit['invalid']) or 'none'}",
            f"- numbers not found in their cited passage: {', '.join(cit['unsupported_numbers']) or 'none'}",
            f"- uncited factual-looking sentences: {len(cit['uncited_sentences'])}",
            f"- insufficient-evidence response: {'yes' if cit['insufficient'] else 'no'}",
            f"- automatic verdict: **{'PASS' if cit['pass'] else 'NEEDS REVIEW'}**",
            "",
            "## Assessment (human, after opening the cited passages)",
            "",
            "_To be written after checking each claim against the original source._",
            "",
            "## Passage text as retrieved",
            "",
            *[f"**[S{i}] {h['source_note']}, {h['locator']}**\n\n" + "\n".join("> " + l for l in h["text"].strip().splitlines()) + "\n"
              for i, h in enumerate(hits, 1)],
        ])
        path = CARDS / f"{test['id']}.md"
        if path.exists():
            # Keep earlier results: a rerun never silently replaces a failed card.
            previous = CARDS / "history"
            previous.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            path.rename(previous / f"{test['id']}-{stamp}.md")
        path.write_text(card + "\n")
        print(f"card     {path.relative_to(ROOT)}")
