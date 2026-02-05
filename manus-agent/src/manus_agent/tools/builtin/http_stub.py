from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from manus_agent.tools.base import Tool, ToolResult


@dataclass
class HttpStubTool(Tool):
    name: str = "http_get_stub"
    description: str = (
        "A safe placeholder for HTTP GET. It does NOT call the network. "
        "Input: {"url": "https://example.com"}"
    )

    def run(self, tool_input: Dict[str, Any]) -> ToolResult:
        url = str(tool_input.get("url", "")).strip()
        if not url:
            return ToolResult(output="Error: missing 'url'.")
        return ToolResult(
            output=(
                "HTTP is disabled in this template (by design). "
                "Replace this stub with a real, sandboxed HTTP client."
            )
        )
