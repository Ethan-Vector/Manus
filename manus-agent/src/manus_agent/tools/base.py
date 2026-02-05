from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ToolResult:
    output: str


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, tool_input: Dict[str, Any]) -> ToolResult:
        raise NotImplementedError
