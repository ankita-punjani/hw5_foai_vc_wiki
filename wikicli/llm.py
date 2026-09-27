"""Local Gemma via MLX. The only module that talks to the model.

Gemma never reads files by itself: callers pass a list of chat messages that
the harness has already assembled (instructions + evidence + question).
"""

from __future__ import annotations

import os
import resource
import sys
import time
from dataclasses import dataclass
from typing import Callable

from .config import WikiError, settings

# Local mode must never reach the network: forbid Hugging Face downloads and
# version checks before any HF/transformers module is imported.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

# The files mlx-lm actually loads (it never fetches README.md or .gitattributes).
RUNTIME_FILES = ["*.json", "*.safetensors", "*.jinja", "*.model", "*.txt"]

THOUGHT_OPEN, THOUGHT_CLOSE = "<|channel>", "<channel|>"


@dataclass
class Generation:
    text: str
    prompt_tokens: int
    generated_tokens: int
    seconds: float
    tokens_per_second: float
    peak_memory_gb: float  # MLX peak (weights + KV cache + activations)
    process_rss_gb: float  # whole Python process, max resident set size

    def summary(self) -> str:
        return (
            f"{self.seconds:.1f}s · {self.prompt_tokens} prompt + {self.generated_tokens} generated tokens "
            f"· {self.tokens_per_second:.0f} tok/s · peak MLX memory {self.peak_memory_gb:.2f} GB"
        )


_CACHE: dict[str, "LocalGemma"] = {}


def get_model(model_id: str | None = None) -> "LocalGemma":
    """One loaded model per process (eval runs several asks; load once)."""
    model_id = model_id or settings()["model"]["id"]
    if model_id not in _CACHE:
        _CACHE[model_id] = LocalGemma(model_id)
    return _CACHE[model_id]


class LocalGemma:
    def __init__(self, model_id: str | None = None):
        self.model_id = model_id or settings()["model"]["id"]
        self._model = self._tokenizer = None
        self.load_seconds: float | None = None

    def load(self) -> None:
        self._load()

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from huggingface_hub import snapshot_download

            snapshot_download(self.model_id, local_files_only=True, allow_patterns=RUNTIME_FILES)
        except Exception:
            raise WikiError(
                f"Local model '{self.model_id}' is not in the Hugging Face cache, so it cannot run offline.\n"
                f"  While online, download it once:  .venv/bin/hf download {self.model_id}\n"
                "  (or change [model].id in config.toml to a Gemma model you have downloaded)."
            ) from None
        from mlx_lm import load

        start = time.time()
        print(f"· loading {self.model_id} (local, MLX) ...", file=sys.stderr, flush=True)
        self._model, self._tokenizer = load(self.model_id)
        self.load_seconds = time.time() - start

    def generate(
        self,
        messages: list[dict],
        max_tokens: int,
        temperature: float,
        on_text: Callable[[str], None] | None = None,
    ) -> Generation:
        """Run one chat completion. `on_text` receives visible text as it streams."""
        self._load()
        import mlx.core as mx
        from mlx_lm import stream_generate
        from mlx_lm.sample_utils import make_sampler

        prompt = self._tokenizer.apply_chat_template(messages, add_generation_prompt=True, enable_thinking=False)
        mx.reset_peak_memory()
        start = time.time()
        raw, shown, last = "", 0, None
        for last in stream_generate(
            self._model, self._tokenizer, prompt, max_tokens=max_tokens, sampler=make_sampler(temp=temperature)
        ):
            raw += last.text
            if on_text:
                visible = _visible(raw, final=False)
                if len(visible) > shown:
                    on_text(visible[shown:])
                    shown = len(visible)
        seconds = time.time() - start
        text = _visible(raw, final=True)
        if on_text and len(text) > shown:
            on_text(text[shown:])
        return Generation(
            text=text.strip(),
            prompt_tokens=last.prompt_tokens if last else 0,
            generated_tokens=last.generation_tokens if last else 0,
            seconds=seconds,
            tokens_per_second=last.generation_tps if last else 0.0,
            peak_memory_gb=mx.get_peak_memory() / 1e9,
            process_rss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9,  # bytes on macOS
        )


def _visible(raw: str, final: bool) -> str:
    """Hide Gemma 4's optional thought channel; only the answer is shown and stored."""
    if THOUGHT_OPEN in raw:
        if THOUGHT_CLOSE not in raw:
            return "" if not final else raw.split(THOUGHT_OPEN, 1)[0]
        return raw.rsplit(THOUGHT_CLOSE, 1)[-1].lstrip()
    # Hold back a partial "<|channel>" marker while streaming.
    if not final and THOUGHT_OPEN.startswith(raw.strip()[:9]) and len(raw.strip()) < 9:
        return ""
    return raw.replace("<end_of_turn>", "").replace("<eos>", "")
