from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional


MessageRole = Literal["system", "user", "assistant", "tool"]


@dataclass
class Message:
    role: MessageRole
    content: str
    name: Optional[str] = None  # for tool messages


@dataclass
class TraceStep:
    step: int
    action_type: str
    tool_name: Optional[str] = None
    tool_input: Optional[Dict[str, Any]] = None
    tool_output: Optional[str] = None
    error: Optional[str] = None


@dataclass
class AgentState:
    messages: List[Message] = field(default_factory=list)
    trace: List[TraceStep] = field(default_factory=list)

    def add_user(self, text: str) -> None:
        self.messages.append(Message(role="user", content=text))

    def add_assistant(self, text: str) -> None:
        self.messages.append(Message(role="assistant", content=text))

    def add_tool_observation(self, tool_name: str, output: str) -> None:
        self.messages.append(Message(role="tool", content=output, name=tool_name))

    def last_user_message(self) -> Optional[str]:
        for m in reversed(self.messages):
            if m.role == "user":
                return m.content
        return None
