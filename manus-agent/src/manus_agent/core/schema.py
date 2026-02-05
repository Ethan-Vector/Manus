from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field


class ToolAction(BaseModel):
    type: Literal["tool"] = "tool"
    tool_name: str = Field(..., min_length=1)
    tool_input: Dict[str, Any] = Field(default_factory=dict)


class FinalAction(BaseModel):
    type: Literal["final"] = "final"
    final: str = Field(..., min_length=1)


Action = ToolAction | FinalAction


class LLMResult(BaseModel):
    raw_text: str
    action: Action
    model: str = "unknown"
