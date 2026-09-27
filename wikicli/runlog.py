"""Saved outputs. Every ask/search/chat/ingest run writes a Markdown record and a
JSON twin to outputs/runs/, labelled with mode and execution setting, so results
can be inspected without rerunning the model."""

from __future__ import annotations

import json
import platform
import time
from datetime import datetime
from pathlib import Path

from .config import ROOT, RUNS, settings


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def environment(execution: str = "local") -> dict:
    s = settings()
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "execution": execution,
        "model": s["model"]["id"],
        "runtime": s["model"]["runtime"] + " " + _version("mlx-lm") + " / mlx " + _version("mlx"),
        "device": f"{platform.machine()} · macOS {platform.mac_ver()[0]}",
        "network": network_state(),
    }


def _version(pkg: str) -> str:
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version(pkg)
    except PackageNotFoundError:
        return "?"


def network_state() -> str:
    """Best-effort check recorded in each log: can we open a socket to the internet?"""
    import socket

    try:
        socket.create_connection(("1.1.1.1", 53), timeout=1.5).close()
        return "online"
    except OSError:
        return "offline (no route to internet)"


def write(kind: str, markdown: str, record: dict, name: str | None = None) -> Path:
    RUNS.mkdir(parents=True, exist_ok=True)
    base = RUNS / f"{name or stamp()}-{kind}"
    n = 2
    while not name and base.with_suffix(".md").exists():  # two runs in the same second
        base = RUNS / f"{stamp()}-{kind}-{n}"
        n += 1
    base.with_suffix(".md").write_text(markdown)
    base.with_suffix(".json").write_text(json.dumps(record, indent=2, ensure_ascii=False, default=str))
    return base.with_suffix(".md")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *exc):
        self.seconds = time.time() - self.start
