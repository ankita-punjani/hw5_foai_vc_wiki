"""Citation checks run on every generated answer.

A citation is not proof by itself, so beyond "does [S3] exist?" we also check
that every number in a cited sentence actually appears in the cited passages.
The checks flag problems; they never rewrite the model's answer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .retrieval import Hit

INSUFFICIENT = re.compile(r"^\W*insufficient evidence", re.I)
_CITE = re.compile(r"\[([SN])(\d+)\]")
_NUMBER = re.compile(
    r"\$?(?:\d[\d,]*(?:\.\d+)?|\.\d+)\+?\s*(?:%|x\b|thousand\b|million\b|billion\b|mm\b|bn\b|k\b|m\b|b\b)?", re.I
)


@dataclass
class CitationReport:
    cited: list[int] = field(default_factory=list)  # 1-based passage numbers actually cited
    invalid: list[str] = field(default_factory=list)  # cited numbers with no such passage
    uncited_sentences: list[str] = field(default_factory=list)
    unsupported_numbers: list[str] = field(default_factory=list)  # "34% (not in S2)"
    insufficient: bool = False

    @property
    def ok(self) -> bool:
        return not (self.invalid or self.unsupported_numbers or (self.uncited_sentences and not self.insufficient))

    def lines(self) -> list[str]:
        out = []
        if self.insufficient:
            out.append("answer reports insufficient evidence")
        out.append(f"cited passages: {', '.join(map(str, self.cited)) or 'none'}")
        if self.invalid:
            out.append(f"INVALID citations (no such passage): {', '.join(self.invalid)}")
        if self.unsupported_numbers:
            out.append(f"numbers NOT found in their cited passage: {', '.join(self.unsupported_numbers)}")
        if self.uncited_sentences:
            out.append(f"{len(self.uncited_sentences)} factual-looking sentence(s) without a citation")
        out.append("citation check: PASS" if self.ok else "citation check: NEEDS REVIEW")
        return out


_UNIT = {"k": 1e3, "thousand": 1e3, "m": 1e6, "mm": 1e6, "million": 1e6, "b": 1e9, "bn": 1e9, "billion": 1e9}


def _norm_number(raw: str) -> str:
    """Canonical value so "$500k", "$500,000" and "0.5 million" compare equal; % and x keep their unit."""
    s = raw.lower().replace(",", "").replace("$", "").replace("+", "").strip()
    m = re.match(r"(\d*\.?\d+)\s*(%|x|thousand|million|billion|mm|bn|k|m|b)?$", s)
    if not m:
        return s
    value, unit = float(m.group(1)), m.group(2) or ""
    if unit in _UNIT:
        return f"{value * _UNIT[unit]:g}"
    return f"{value:g}{unit}"


def _numbers(text: str) -> dict[str, str]:
    """canonical value -> the number as written. "20 percent" counts as "20%"."""
    text = re.sub(r"(\d)\s*percent\b", r"\1%", text, flags=re.I)
    return {_norm_number(n): n.strip() for n in _NUMBER.findall(text) if re.search(r"\d", n)}


def passage_values(text: str) -> set[str]:
    """Canonical numbers in a passage. Slide tables often list multiples without the "x"
    ("Multiple 25 5 1.4"), so in passages that talk about multiples a bare number also counts as "Nx"."""
    values = set(_numbers(text))
    if re.search(r"\bmultiples?\b", text, re.I):
        values |= {f"{v}x" for v in values if re.fullmatch(r"\d*\.?\d+", v)}
    return values


def supported(value: str, available: set[str]) -> bool:
    """A bare number in an answer matches the same multiple in the source ("53.3" vs "53.3x")."""
    return value in available or (not value.endswith("x") and f"{value}x" in available)


def _sentences(text: str) -> list[str]:
    text = re.sub(r"^\s*[-*•]\s+", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) > 25]


def check(answer: str, hits: list[Hit], tag: str = "S") -> CitationReport:
    report = CitationReport(insufficient=bool(INSUFFICIENT.search(answer)))
    passages_numbers = [passage_values(h.passage.text + " " + h.passage.locator) for h in hits]
    for sentence in _sentences(answer):
        cites = [int(n) for t, n in _CITE.findall(sentence) if t == tag]
        for n in cites:
            if not 1 <= n <= len(hits):
                report.invalid.append(f"[{tag}{n}]")
            elif n not in report.cited:
                report.cited.append(n)
        valid = [n for n in cites if 1 <= n <= len(hits)]
        if not cites:
            # Headings, restated questions and "insufficient" lines need no citation.
            if not INSUFFICIENT.search(sentence) and re.search(r"\d|\b(is|are|was|were|has|have)\b", sentence):
                report.uncited_sentences.append(sentence)
            continue
        claimed = _numbers(_CITE.sub("", sentence))
        available = set().union(*(passages_numbers[n - 1] for n in valid)) if valid else set()
        for num, written in sorted(claimed.items()):
            if num and not supported(num, available) and not _trivial(num):
                report.unsupported_numbers.append(f"{written} (not in {', '.join(f'{tag}{n}' for n in valid)})")
    report.cited.sort()
    return report


def _trivial(num: str) -> bool:
    """Step numbers and small counts ("Step 1", "3 steps") are not factual claims."""
    return re.fullmatch(r"\d+", num) is not None and int(num) <= 10
