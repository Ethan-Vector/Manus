from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class OutputPolicy:
    max_chars: int = 2500

    def apply(self, text: str) -> str:
        text = text.strip()
        if not text:
            return "I don't have an answer."
        if len(text) > self.max_chars:
            return text[: self.max_chars].rstrip() + "…"
        return text
