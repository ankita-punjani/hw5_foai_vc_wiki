"""Prompt assembly. Each mode loads its own instruction file; nothing is shared
implicitly, so ask never sees the chat persona and chat never sees ask's rules."""

from __future__ import annotations

from .config import instruction
from .retrieval import Hit


def evidence_block(hits: list[Hit], tag: str) -> str:
    """Numbered passages, each labelled with its source and location."""
    parts = []
    for i, hit in enumerate(hits, start=1):
        p = hit.passage
        parts.append(f"[{tag}{i}] Source: {p.source_note} ({p.source_file}), {p.locator}\n{p.text.strip()}")
    return "\n\n".join(parts)


def ask_messages(question: str, hits: list[Hit], unknown_terms: list[str] | None = None) -> list[dict]:
    """Ask mode: research rules + evidence + one standalone question. No history, no persona.

    `unknown_terms` are question words that occur in none of the sources; the harness knows this
    from the index and tells the model, so it cannot quietly answer about something never mentioned."""
    evidence = evidence_block(hits, "S") if hits else "(no passages matched the question)"
    note = ""
    if unknown_terms:
        note = (f"PROGRAM NOTE: these words from the question appear nowhere in the sources: {', '.join(unknown_terms)}. "
                "An everyday word may just be a synonym for something the passages describe in other words; then answer "
                "from the passages. But if the question asks about a specific term, rule, number, or instrument that the "
                "passages never mention, start with INSUFFICIENT EVIDENCE (rule 6) and do not define or explain it.\n\n")
    return [
        {"role": "system", "content": instruction("wiki-instructions.md")},
        {
            "role": "user",
            "content": f"EVIDENCE PASSAGES:\n\n{evidence}\n\n{note}QUESTION: {question}\n\n"
            "Answer using only the evidence passages, citing them like [S1].",
        },
    ]


def chat_messages(history: list[dict], message: str, hits: list[Hit] | None, retrieval_note: str) -> list[dict]:
    """Chat mode: persona + recent conversation + (optionally) notes for this turn only."""
    system = instruction("persona.md")
    messages = [{"role": "system", "content": system}, *history]
    if hits:
        user = (
            "NOTES (looked up automatically by the program from the wiki's original sources — not written or "
            "sent by me; use only the ones relevant to my message and cite them as [N1], [N2] ...):\n\n"
            f"{evidence_block(hits, 'N')}\n\n"
            f"MY MESSAGE (answer this directly first): {message}"
        )
    else:
        user = f"(No notes were looked up for this message: {retrieval_note}.)\n\nMY MESSAGE: {message}"
    messages.append({"role": "user", "content": user})
    return messages


def ingest_messages(topic_name: str, description: str, hits: list[Hit]) -> list[dict]:
    return [
        {"role": "system", "content": instruction("ingest-instructions.md")},
        {
            "role": "user",
            "content": f"TOPIC: {topic_name} — {description}\n\nEVIDENCE PASSAGES:\n\n{evidence_block(hits, 'S')}\n\n"
            f"Write the page for the topic '{topic_name}'.",
        },
    ]


def source_overview_messages(title: str, outline: str) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You describe a source document for a study wiki in 3 plain sentences: what it is, "
            "what it covers, and who it is useful for. Use only the outline given. No lists, no headings.",
        },
        {"role": "user", "content": f"SOURCE: {title}\n\nOUTLINE (section titles and first lines):\n{outline}"},
    ]
