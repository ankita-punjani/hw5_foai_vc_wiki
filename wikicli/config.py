"""Paths and settings shared by every command."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
RAW = VAULT / "raw"
WIKI = VAULT / "wiki"
INDEX_MD = VAULT / "index.md"
INSTRUCTIONS = ROOT / "instructions"
DATA = ROOT / "data"  # machine files: passages, drafts — never inside the vault
INDEX_DIR = DATA / "index"
DRAFTS = DATA / "drafts"
OUTPUTS = ROOT / "outputs"
RUNS = OUTPUTS / "runs"  # automatic logs of every ask/search/chat/ingest run
SAVED = OUTPUTS / "saved"  # replies the user explicitly /save'd in chat


class WikiError(Exception):
    """A user-facing error: printed without a traceback."""


@cache
def settings() -> dict:
    with (ROOT / "config.toml").open("rb") as f:
        return tomllib.load(f)


@dataclass(frozen=True)
class Source:
    id: str
    file: str
    note: str
    title: str
    author: str
    published: str
    kind: str
    url: str
    original_filename: str
    exclude_pages: tuple[int, ...]
    license_note: str
    strip_patterns: tuple[str, ...] = ()

    @property
    def path(self) -> Path:
        return RAW / self.file

    @property
    def rel(self) -> str:
        return f"raw/{self.file}"


@cache
def sources() -> dict[str, Source]:
    """Source catalog keyed by vault-relative path ("raw/<file>")."""
    entries = yaml.safe_load((ROOT / "sources.yml").read_text())["sources"]
    out = {}
    for e in entries:
        e["exclude_pages"] = tuple(e.get("exclude_pages") or ())
        e["strip_patterns"] = tuple(e.get("strip_patterns") or ())
        s = Source(**e)
        out[s.rel] = s
    return out


def source_for(path: Path) -> Source:
    rel = f"raw/{path.name}"
    catalog = sources()
    if rel not in catalog:
        raise WikiError(
            f"{path.name} is not in sources.yml. Add an entry (id, file, note, title, author, ...) "
            "so the source gets a readable wiki name and a stable ID, then ingest again."
        )
    return catalog[rel]


@cache
def topics() -> dict:
    return yaml.safe_load((INSTRUCTIONS / "topics.yml").read_text())


def instruction(name: str) -> str:
    path = INSTRUCTIONS / name
    if not path.exists():
        raise WikiError(f"Missing instruction file {path.relative_to(ROOT)}")
    return path.read_text().strip()
