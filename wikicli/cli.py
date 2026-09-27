"""`wiki` command line. Parses the command, picks the mode, and hands off to the harness."""

from __future__ import annotations

import argparse
import sys

from .config import ROOT, WikiError

DESCRIPTION = """\
Personal VC-math wiki powered by a local Gemma model (offline by default).

commands:
  ingest [PATH ...]   read originals in vault/raw/, index passages, draft/update wiki notes, rebuild index.md
  search "QUERY"      show matching ORIGINAL passages + source paths (no language model)
  ask "QUESTION"      standalone factual answer from retrieved evidence, with citations
  chat                talk with Carry, a study-partner persona that uses the conversation and looks up notes when useful
  eval                run the four ask-mode tests in tests/questions.yml and write evidence cards
  verify              audit every wiki note: footnotes resolve to sources, numbers appear in the cited passage
  status              show model, index, vault, and network status
  help [COMMAND]      show help (same as --help)

execution:
  --mode local        (default) Gemma 4 E2B via MLX from the local Hugging Face cache; never uses the network
  --mode online       not configured in this project; local is the required, complete path

inputs:
  vault/raw/          unchanged original sources (.pdf .epub .md .txt), each registered in sources.yml
  instructions/       wiki-instructions.md (ask rules), persona.md (chat), ingest-instructions.md, topics.yml
  config.toml         model id, generation settings, passage size, top-k

examples:
  wiki ingest vault/raw
  wiki search "return the fund"
  wiki ask "What check size range does Harlem Capital write?"
  wiki chat
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wiki", description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p = sub.add_parser("ingest", help="index sources and build wiki notes")
    p.add_argument("paths", nargs="*", help="files or folders inside vault/raw/ (default: vault/raw)")
    p.add_argument("--force", action="store_true", help="regenerate draft notes even if their evidence is unchanged")
    p.add_argument("--redraft", action="store_true", help="also redraft reviewed notes, into data/drafts/ (reviewed notes are never overwritten)")
    p.add_argument("--no-llm", action="store_true", help="only extract and index passages; do not call Gemma")

    p = sub.add_parser("search", help="retrieval only: matching original passages, no generated answer")
    p.add_argument("query")
    p.add_argument("-k", type=int, help="number of passages (default from config.toml)")
    p.add_argument("--scope", choices=["raw", "wiki", "all"], default="raw", help="raw = original sources (default), wiki = generated notes")
    p.add_argument("--full", action="store_true", help="print whole passages")

    p = sub.add_parser("ask", help="standalone, cited answer from the original sources")
    p.add_argument("question")
    p.add_argument("-k", type=int, help="passages given to Gemma (default from config.toml)")
    p.add_argument("--show-context", action="store_true", help="print the retrieved passages in full")
    p.add_argument("--mode", choices=["local", "online"], default="local")

    p = sub.add_parser("chat", help="personal assistant with conversation context")
    p.add_argument("--mode", choices=["local", "online"], default="local")
    p.add_argument("--script", help="read user messages from a file, one per line (for reproducible transcripts)")

    p = sub.add_parser("eval", help="run the ask-mode test set and write evidence cards")
    p.add_argument("--tests", default=str(ROOT / "tests" / "questions.yml"))
    p.add_argument("--only", nargs="*", help="test ids to run, e.g. T1 T4")

    sub.add_parser("verify", help="audit wiki notes against the passages they cite (no model)")
    sub.add_parser("status", help="model, index, vault, and network status")
    p = sub.add_parser("help", help="show help")
    p.add_argument("topic", nargs="?")
    return parser


def require_local(mode: str) -> None:
    if mode == "online":
        raise WikiError(
            "Online mode is not configured in this project. The required local mode is the default: "
            "rerun without --mode online (or with --mode local)."
        )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command in (None, "help"):
            topic = getattr(args, "topic", None)
            if topic:
                parser.parse_args([topic, "--help"])
            parser.print_help()
            return 0
        if args.command == "ingest":
            from .ingest import run

            run(args.paths, force=args.force, redraft=args.redraft, no_llm=args.no_llm)
        elif args.command == "search":
            from .modes import search

            search(args.query, k=args.k, scope=args.scope, full=args.full)
        elif args.command == "ask":
            require_local(args.mode)
            from .modes import ask

            ask(args.question, k=args.k, show_context=args.show_context)
        elif args.command == "chat":
            require_local(args.mode)
            from .chat import run

            run(script=args.script)
        elif args.command == "eval":
            from .evaluate import run

            run(args.tests, args.only)
        elif args.command == "verify":
            from .verify import run

            return run()
        elif args.command == "status":
            from .status import run

            run()
        return 0
    except WikiError as e:
        print(f"wiki: error: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:
        print(f"wiki: error: {e}", file=sys.stderr)
        return 2
