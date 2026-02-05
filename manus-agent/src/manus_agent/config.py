from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from typing import Literal


@dataclass(frozen=True)
class ManusConfig:
    llm_provider: Literal["mock", "openai"] = "mock"
    max_steps: int = 6
    log_level: str = "INFO"

    @staticmethod
    def from_env() -> "ManusConfig":
        provider = getenv("MANUS_LLM_PROVIDER", "mock").strip().lower()
        max_steps = int(getenv("MANUS_MAX_STEPS", "6"))
        log_level = getenv("MANUS_LOG_LEVEL", "INFO").strip().upper()
        if provider not in {"mock", "openai"}:
            provider = "mock"
        return ManusConfig(llm_provider=provider, max_steps=max_steps, log_level=log_level)
