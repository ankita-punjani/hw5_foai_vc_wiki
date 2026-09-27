"""Chat mode: the "Carry" persona with conversation memory and optional retrieval.

The harness, not the model, decides whether to look up notes for each message
(see `decide_retrieval`). Notes are attached to the current turn only; the
history keeps the user's words and the assistant's replies, with note citations
rewritten into readable labels so follow-ups can keep them.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

from . import runlog
from .config import SAVED, instruction, settings
from .modes import DIM, RESET, hit_record
from .citations import check
from .prompts import chat_messages
from .retrieval import Hit, load_index

GREETING = re.compile(r"^\s*(hi|hey|hello|yo|thanks|thank you|thx|ok(ay)?|cool|great|nice|bye)\b", re.I)
META = re.compile(
    r"what can (you|we|i)\b|help me with|who are you|what are you|what do you do|how do(es)? (this|you) work|"
    r"your (capabilities|commands)|what('s| is) (this|your) (tool|job)",
    re.I,
)
FOLLOW_UP = re.compile(
    r"\b(make (it|that|this|them)|shorter|longer|shorten|simpler|simplify|more simply|in plain|plain english|eli5|"
    r"explain (it|that|this)|say (it|that|this)|rephrase|reword|rewrite|turn (it|that|this) into|as bullets|"
    r"bullet points|more concise|tl;?dr|another version|try again|expand on (it|that|this))\b",
    re.I,
)

HELP = """commands:
  /notes <message>    force a notes lookup for this message
  /nonotes <message>  answer without looking up notes
  /save               save the last reply to outputs/saved/ (marked as a generated draft, not evidence)
  /reset              forget the conversation so far
  /help               show this list
  /exit               quit (Ctrl-D also works)"""


def decide_retrieval(message: str, has_history: bool) -> tuple[bool | None, str]:
    """(True/False, reason) from the message alone, or (None, "") to let coverage decide."""
    words = len(message.split())
    if GREETING.search(message) and words <= 6:
        return False, "casual message"
    if META.search(message) and words <= 16:
        return False, "question about the assistant itself"
    if has_history and FOLLOW_UP.search(message) and words <= 16:
        return False, "follow-up that reworks the previous reply"
    return None, ""


class Chat:
    def __init__(self, execution: str = "local"):
        from .llm import get_model

        self.cfg = settings()
        self.execution = execution
        self.gemma = get_model()
        self.history: list[dict] = []
        self.transcript: list[str] = []
        self.turns: list[dict] = []
        self.last_reply: dict | None = None
        instruction("persona.md")  # fail early if the persona file is missing

    # -- history ---------------------------------------------------------------

    def trimmed_history(self) -> list[dict]:
        c = self.cfg["chat"]
        recent = self.history[-2 * c["history_turns"]:]
        while recent and sum(len(m["content"]) for m in recent) > c["history_chars"]:
            recent = recent[2:]
        return recent

    # -- one turn --------------------------------------------------------------

    def turn(self, message: str) -> str:
        force = None
        if message.startswith("/notes "):
            force, message = True, message[len("/notes "):]
        elif message.startswith("/nonotes "):
            force, message = False, message[len("/nonotes "):]

        hits: list[Hit] = []
        if force is False:
            decision, reason = False, "you asked for no notes"
        elif force is True:
            decision, reason = True, "you asked for a notes lookup"
        else:
            decision, reason = decide_retrieval(message, bool(self.history))
        if decision is not False:
            found = load_index("raw").search(message, k=self.cfg["retrieval"]["chat_top_k"])
            need = self.cfg["retrieval"]["chat_min_coverage"]
            best = found[0].coverage if found else 0.0
            if decision is True:
                hits = found
            elif best >= need:
                hits = [h for h in found if h.coverage >= need * 0.6]
                reason = f"message matches the notes (best coverage {best:.0%})"
            else:
                reason = f"no note matches this well (best coverage {best:.0%} < {need:.0%})"

        status = f"notes: searched, {len(hits)} passages — {reason}" if hits else f"notes: not searched — {reason}"
        if not hits and force is None and reason.startswith("follow-up") and self.last_reply and self.last_reply["hits"]:
            # A rewrite of the previous answer keeps that answer's evidence in view, so rewording
            # cannot drift away from the notes (and the citation check still applies).
            hits = self.last_reply["hits"]
            status = f"notes: reused {len(hits)} passages from the previous answer — {reason}"
        print(f"{DIM}· {status}{RESET}")
        messages = chat_messages(self.trimmed_history(), message, hits, reason)

        self.gemma.load()  # so the one-time "loading" line never lands mid-reply
        print("carry> ", end="", flush=True)
        gen = self.gemma.generate(
            messages, self.cfg["generation"]["chat_max_tokens"], self.cfg["generation"]["chat_temperature"],
            on_text=lambda s: print(s, end="", flush=True),
        )
        print()
        reply = gen.text
        cited = sorted({int(n) for n in re.findall(r"\[N(\d+)\]", reply) if 1 <= int(n) <= len(hits)})
        if cited:
            print(f"{DIM}  notes cited:{RESET}")
            for n in cited:
                p = hits[n - 1].passage
                print(f"{DIM}  [N{n}] {p.source_note} — {p.source_file}, {p.locator}{RESET}")
        # Same safety net as ask mode: a cited number must appear in the cited note. If it does not,
        # the harness sends the reply back once with the exact problem and shows the corrected version.
        warnings = check(reply, hits, "N").unsupported_numbers if hits else []
        first_reply = None
        if warnings:
            for w in warnings:
                print(f"  ⚠ citation check: {w}: the cited note does not contain this number; asking Carry to correct it")
            first_reply = reply
            retry = messages + [
                {"role": "assistant", "content": reply},
                {"role": "user", "content": "PROGRAM CHECK (not from me): your reply cites notes for numbers those notes do not "
                 f"contain: {'; '.join(warnings)}. Rewrite the reply. Every number you cite must appear in the cited note. "
                 "If what I said conflicts with the notes, tell me so and give the notes' figure with its citation."},
            ]
            print("carry (corrected)> ", end="", flush=True)
            gen = self.gemma.generate(retry, self.cfg["generation"]["chat_max_tokens"], 0.0,
                                      on_text=lambda s: print(s, end="", flush=True))
            print()
            reply = gen.text
            warnings = check(reply, hits, "N").unsupported_numbers
            for w in warnings:
                print(f"  ⚠ citation check (still): {w}")
            cited = sorted({int(n) for n in re.findall(r"\[N(\d+)\]", reply) if 1 <= int(n) <= len(hits)})
        load = f" (+{self.gemma.load_seconds:.1f}s model load)" if self.gemma.load_seconds and not self.turns else ""
        print(f"{DIM}  {gen.summary()}{load}{RESET}\n")

        # Store the reply with readable citations so later turns can keep them.
        stored = re.sub(
            r"\[N(\d+)\]",
            lambda m: f"[{hits[int(m.group(1)) - 1].passage.label}]" if 1 <= int(m.group(1)) <= len(hits) else "",
            reply,
        )
        self.history += [{"role": "user", "content": message}, {"role": "assistant", "content": stored}]
        self.last_reply = {"message": message, "reply": stored, "hits": hits}
        self.turns.append({
            "user": message, "retrieval": status, "hits": [hit_record(h) for h in hits],
            "reply": reply, "first_reply_before_citation_fix": first_reply, "cited": cited,
            "citation_warnings": warnings, "generation": gen.__dict__,
        })
        self.transcript += [f"**you:** {message}", "", f"_{status}_", ""]
        if first_reply:
            self.transcript += [f"**carry (first reply, failed the citation check):** {first_reply}", "",
                                "_⚠ harness: a cited number was not in the cited note; reply sent back once for correction_", ""]
        self.transcript += [f"**carry:** {reply}", ""]
        if cited:
            self.transcript += [*(f"- [N{n}] {hits[n - 1].passage.label} — `{hits[n - 1].passage.source_file}`" for n in cited), ""]
        if warnings:
            self.transcript += [*(f"- ⚠ citation check: {w}" for w in warnings), ""]
        self.transcript += [f"<sub>{gen.summary()}</sub>", ""]
        return reply

    # -- commands --------------------------------------------------------------

    def save_last(self) -> None:
        if not self.last_reply:
            print("nothing to save yet.")
            return
        SAVED.mkdir(parents=True, exist_ok=True)
        slug = re.sub(r"[^a-z0-9]+", "-", self.last_reply["message"].lower()).strip("-")[:40] or "reply"
        path = SAVED / f"{datetime.now():%Y%m%d-%H%M%S} {slug}.md"
        notes = "\n".join(f"- {h.passage.label} — `{h.passage.source_file}`" for h in self.last_reply["hits"]) or "- none"
        path.write_text(
            "---\nkind: generated-draft\nevidence: false  # chat output; ask mode never retrieves this folder\n"
            f"model: {self.gemma.model_id}\nsaved_at: {datetime.now().isoformat(timespec='seconds')}\n---\n"
            f"# {self.last_reply['message']}\n\n{self.last_reply['reply']}\n\n## Notes shown to the model\n{notes}\n"
        )
        print(f"{DIM}saved to {runlog.rel(path)} (outside the vault; not used as evidence){RESET}")

    def finish(self) -> Path | None:
        if not self.turns:
            return None
        env = runlog.environment(self.execution)
        md = "\n".join([
            "# Chat transcript",
            "",
            f"- **Mode:** chat (persona: Carry, conversation context, retrieval only when needed) · **Execution:** {self.execution} · **Network:** {env['network']}",
            f"- **Model:** `{env['model']}` · **Runtime:** {env['runtime']} · **Device:** {env['device']}",
            f"- **Started:** {env['timestamp']}",
            "",
            *self.transcript,
        ])
        out = runlog.write("chat", md, {"mode": "chat", "env": env, "turns": self.turns})
        print(f"{DIM}transcript saved to {runlog.rel(out)}{RESET}")
        return out


def run(execution: str = "local", script: str | None = None) -> None:
    chat = Chat(execution)
    print(f"{DIM}wiki chat · persona: Carry · execution: {execution} · model: {chat.gemma.model_id}{RESET}")
    print("Hi, I'm Carry, your VC-math study partner. Ask me anything, or type /help. /exit to quit.\n")
    lines = Path(script).read_text().splitlines() if script else None
    try:
        while True:
            if lines is not None:
                if not lines:
                    break
                message = lines.pop(0).strip()
                if not message or message.startswith("#"):
                    continue
                print(f"you> {message}")
            else:
                try:
                    message = input("you> ").strip()
                except EOFError:
                    print()
                    break
            if not message:
                continue
            if message in ("/exit", "/quit"):
                break
            if message == "/help":
                print(HELP + "\n")
            elif message == "/reset":
                chat.history.clear()
                print(f"{DIM}conversation cleared.{RESET}\n")
            elif message == "/save":
                chat.save_last()
            elif message.startswith("/") and not message.startswith(("/notes ", "/nonotes ")):
                print(f"unknown command {message.split()[0]!r}. Type /help.\n")
            else:
                chat.turn(message)
    except KeyboardInterrupt:
        print()
    finally:
        chat.finish()
