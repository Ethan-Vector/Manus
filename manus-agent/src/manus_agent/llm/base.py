from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any

from manus_agent.core.schema import LLMResult
from manus_agent.core.state import Message


class LLM(ABC):
    @abstractmethod
    def complete(self, messages: List[Message], tools: List[Dict[str, str]]) -> LLMResult:
        raise NotImplementedError
