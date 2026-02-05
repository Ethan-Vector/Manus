from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from manus_agent.tools.base import Tool, ToolResult


class ToolNotFound(Exception):
    pass


@dataclass
class ToolRegistry:
    tools: Dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def list(self) -> List[Dict[str, str]]:
        return [{"name": t.name, "description": t.description} for t in self.tools.values()]

    def run(self, name: str, tool_input: Dict[str, Any]) -> ToolResult:
        tool = self.tools.get(name)
        if tool is None:
            raise ToolNotFound(f"Tool not found: {name}")
        return tool.run(tool_input)
