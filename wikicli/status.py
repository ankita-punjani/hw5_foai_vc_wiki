"""`wiki status`: what is installed, indexed, and generated — without loading the model."""

from __future__ import annotations

import json
import os
from pathlib import Path

from . import runlog
from .llm import RUNTIME_FILES
from .config import INDEX_DIR, INDEX_MD, RAW, ROOT, settings, sources


def run() -> None:
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    s = settings()
    model = s["model"]["id"]
    try:
        from huggingface_hub import snapshot_download

        path = snapshot_download(model, local_files_only=True, allow_patterns=RUNTIME_FILES)
        size = sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file()) / 1e9
        model_state = f"cached locally ({size:.1f} GB) at {path}"
    except Exception:
        model_state = "NOT cached — download it while online (see README)"
    env = runlog.environment()
    print(f"model      {model}\n           {model_state}")
    print(f"runtime    {env['runtime']}")
    print(f"device     {env['device']}")
    print(f"network    {env['network']}  (local mode does not use it)")
    print("sources")
    for src in sources().values():
        meta_file = INDEX_DIR / "raw" / f"{src.id}.meta.json"
        state = "missing file!" if not src.path.exists() else "not indexed"
        if meta_file.exists() and src.path.exists():
            m = json.loads(meta_file.read_text())
            state = f"{m['passages']} passages, indexed {m['indexed_at']}"
        print(f"  {src.rel:48} {state}")
    unregistered = [p.name for p in RAW.iterdir() if p.is_file() and p.name != "README.md" and f"raw/{p.name}" not in sources()] if RAW.exists() else []
    if unregistered:
        print(f"  unregistered in sources.yml: {', '.join(unregistered)}")
    from .ingest import existing_notes

    notes = existing_notes()
    concept = [n for n in notes.values() if n.meta.get("type") == "concept"]
    reviewed = sum(1 for n in concept if n.meta.get("status") == "reviewed")
    print(f"wiki       {len(concept)} topic notes ({reviewed} reviewed, {len(concept) - reviewed} draft), "
          f"{len(notes) - len(concept)} source notes · index.md {'present' if INDEX_MD.exists() else 'missing'}")
    total, problems = check_links()
    print(f"links      {total} wikilinks checked · {len(problems)} missing or ambiguous")
    for line in problems[:20]:
        print(f"  {line}")
    print(f"project    {ROOT}")


def check_links() -> tuple[int, list[str]]:
    """Resolve every [[wikilink]] in the vault the way Obsidian does (by note name or vault path)."""
    import re

    from .config import VAULT

    files = [p for p in VAULT.rglob("*") if p.is_file() and ".obsidian" not in p.parts]
    by_name: dict[str, list] = {}
    for p in files:
        by_name.setdefault(p.stem if p.suffix == ".md" else p.name, []).append(p)
    paths = {p.relative_to(VAULT).as_posix() for p in files}
    total, problems = 0, []
    for note in VAULT.rglob("*.md"):
        if ".obsidian" in note.parts:
            continue
        for target in re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]", note.read_text()):
            total += 1
            where = note.relative_to(VAULT).as_posix()
            if target in paths or f"{target}.md" in paths:
                continue
            matches = by_name.get(target, [])
            if not matches:
                problems.append(f"{where}: [[{target}]] → missing")
            elif len(matches) > 1:
                problems.append(f"{where}: [[{target}]] → ambiguous ({len(matches)} files)")
    return total, problems
