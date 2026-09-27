"""Search mode (retrieval only) and ask mode (standalone RAG)."""

from __future__ import annotations

import re
import sys
import textwrap

from . import runlog
from .citations import check
from .config import settings
from .prompts import ask_messages
from .retrieval import Hit, load_index, query_terms

BOLD, DIM, RESET = ("\033[1m", "\033[2m", "\033[0m") if sys.stdout.isatty() else ("", "", "")


def highlight(text: str, terms: list[str]) -> str:
    if not BOLD or not terms:
        return text
    pattern = re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")\w*", re.I)
    return pattern.sub(lambda m: BOLD + m.group(0) + RESET, text)


def show_passage(n: str, hit: Hit, full: bool, width: int = 100) -> str:
    p = hit.passage
    text = re.sub(r"\s+", " ", p.text).strip()
    if not full and len(text) > 650:
        text = text[:650].rsplit(" ", 1)[0] + " …"
    body = textwrap.fill(text, width=width, initial_indent="    ", subsequent_indent="    ")
    return (
        f"{n} {p.label}\n"
        f"    {DIM}{p.source_file} · score {hit.score:.2f} · covers {hit.coverage:.0%} of query terms{RESET}\n"
        f"{highlight(body, hit.matched)}"
    )


def passages_markdown(hits: list[Hit], tag: str) -> str:
    out = []
    for i, h in enumerate(hits, 1):
        p = h.passage
        quoted = "\n".join("> " + line for line in p.text.strip().splitlines())
        out.append(f"**[{tag}{i}] {p.label}** — `{p.source_file}` · score {h.score:.2f} · coverage {h.coverage:.0%} · id `{p.id}`\n\n{quoted}\n")
    return "\n".join(out)


def hit_record(h: Hit) -> dict:
    p = h.passage
    return {"id": p.id, "source_note": p.source_note, "file": p.source_file, "locator": p.locator,
            "score": round(h.score, 3), "coverage": round(h.coverage, 3), "matched_terms": h.matched, "text": p.text}


# --- search ------------------------------------------------------------------


def search(query: str, k: int | None = None, scope: str = "raw", full: bool = False) -> list[Hit]:
    k = k or settings()["retrieval"]["search_top_k"]
    with runlog.Timer() as t:
        index = load_index(scope)
        hits = index.search(query, k=k)
    label = {"raw": "original sources (evidence)", "wiki": "generated wiki notes", "all": "sources + wiki notes"}[scope]
    print(f"{DIM}wiki search · retrieval only, no language model · scope: {label} · {index.n} passages · {t.seconds * 1000:.0f} ms{RESET}")
    print(f"query: {query!r} → terms: {', '.join(query_terms(query))}\n")
    if not hits:
        print("No matching passages.")
    for i, h in enumerate(hits, 1):
        print(show_passage(f"[{i}]", h, full) + "\n")
    md = (f"# wiki search\n\n- query: `{query}`\n- scope: {label}\n- model: none (retrieval only)\n"
          f"- network: {runlog.network_state()}\n- time: {t.seconds * 1000:.0f} ms\n\n" + passages_markdown(hits, "R"))
    out = runlog.write("search", md, {"query": query, "scope": scope, "hits": [hit_record(h) for h in hits]})
    print(f"{DIM}saved {runlog.rel(out)}{RESET}")
    return hits


# --- ask ---------------------------------------------------------------------


def ask(question: str, k: int | None = None, show_context: bool = False, execution: str = "local", tag: str | None = None) -> dict:
    """Standalone research answer: retrieve -> prompt with research rules -> Gemma -> citation check.

    Deliberately takes no history and never loads the chat persona."""
    cfg = settings()
    k = k or cfg["retrieval"]["ask_top_k"]
    env = runlog.environment(execution)
    print(f"{DIM}wiki ask · research mode (standalone, no chat history) · execution: {execution} · model: {env['model']}{RESET}")
    print(f"question: {question}\n")

    with runlog.Timer() as t_ret:
        index = load_index("raw")
        hits = index.search(question, k=k)
        unknown = index.unknown_terms(question)
    print(f"retrieved {len(hits)} passages from the original sources ({t_ret.seconds * 1000:.0f} ms):")
    for i, h in enumerate(hits, 1):
        print(f"  [S{i}] {h.passage.label}  {DIM}score {h.score:.2f} · covers {h.coverage:.0%}{RESET}")
    if show_context:
        print()
        for i, h in enumerate(hits, 1):
            print(show_passage(f"[S{i}]", h, full=True) + "\n")
    print()

    from .llm import get_model

    if unknown:
        print(f"  {DIM}· question words found in no source: {', '.join(unknown)} (told to the model){RESET}")
    messages = ask_messages(question, hits, unknown)
    gemma = get_model()
    already_loaded = gemma.load_seconds is not None
    gemma.load()
    print("answer:")
    gen = gemma.generate(messages, cfg["generation"]["ask_max_tokens"], cfg["generation"]["ask_temperature"],
                         on_text=lambda s: print(s, end="", flush=True))
    print("\n")
    report = check(gen.text, hits, "S")
    cited = [hits[n - 1] for n in report.cited]
    if cited:
        print("sources cited:")
        for n in report.cited:
            h = hits[n - 1]
            print(f"  [S{n}] {h.passage.source_note} — {h.passage.source_file}, {h.passage.locator}")
    for line in report.lines():
        print(f"  {DIM}·{RESET} {line}")
    load = f" (+{gemma.load_seconds:.1f}s model load)" if gemma.load_seconds and not already_loaded else ""
    print(f"{DIM}generation: {gen.summary()}{load} · process max RSS {gen.process_rss_gb:.2f} GB{RESET}")

    record = {
        "mode": "ask", "execution": execution, "env": env, "question": question,
        "retrieval": {"top_k": k, "seconds": t_ret.seconds, "hits": [hit_record(h) for h in hits], "unknown_terms": unknown},
        "prompt_messages": messages, "answer": gen.text,
        "citations": {"cited": report.cited, "invalid": report.invalid, "unsupported_numbers": report.unsupported_numbers,
                      "uncited_sentences": report.uncited_sentences, "insufficient": report.insufficient, "pass": report.ok},
        "generation": gen.__dict__, "model_load_seconds": None if already_loaded else gemma.load_seconds,
    }
    md = ask_markdown(record, hits, report)
    out = runlog.write("ask", md, record, name=tag)
    print(f"{DIM}saved {runlog.rel(out)}{RESET}")
    record["saved"] = str(out)
    return record


def ask_markdown(r: dict, hits: list[Hit], report) -> str:
    env, gen = r["env"], r["generation"]
    lines = [
        f"# Ask: {r['question']}",
        "",
        f"- **Mode:** ask (standalone research, no chat history) · **Execution:** {r['execution']} · **Network:** {env['network']}",
        f"- **Model:** `{env['model']}` · **Runtime:** {env['runtime']} · **Device:** {env['device']}",
        f"- **Timing:** retrieval {r['retrieval']['seconds'] * 1000:.0f} ms · generation {gen['seconds']:.1f}s "
        f"({gen['prompt_tokens']} prompt + {gen['generated_tokens']} generated tokens, {gen['tokens_per_second']:.0f} tok/s)"
        + (f" · model load {r['model_load_seconds']:.1f}s" if r["model_load_seconds"] else ""),
        f"- **Memory:** peak MLX {gen['peak_memory_gb']:.2f} GB · process max RSS {gen['process_rss_gb']:.2f} GB",
        f"- **Timestamp:** {env['timestamp']}",
        "",
        "## Answer (verbatim Gemma output)",
        "",
        r["answer"],
        "",
        "## Citations",
        "",
        *[f"- [S{n}] {hits[n - 1].passage.source_note} — `{hits[n - 1].passage.source_file}`, {hits[n - 1].passage.locator}" for n in report.cited],
        "",
        "Automatic check:",
        "",
        *[f"- {line}" for line in report.lines()],
        *([f"  - uncited: “{s}”" for s in report.uncited_sentences]),
        "",
        f"## Retrieved passages (top {len(hits)}, BM25 over original sources)",
        "",
        passages_markdown(hits, "S"),
    ]
    return "\n".join(lines)
