from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Dict, List

from manus_agent.core.schema import FinalAction, LLMResult, ToolAction
from manus_agent.core.state import Message
from manus_agent.llm.base import LLM


@dataclass
class MockLLM(LLM):
    """Mock deterministico: utile per demo ed evals offline.

    Regole:
    - se l'utente scrive: "calc: 2+2" => tool calc
    - se l'utente scrive: "use <tool> {json}" => tool generico
    - altrimenti => risposta finale semplice
    """

    model_name: str = "mock-llm"

    def complete(self, messages: List[Message], tools: List[Dict[str, str]]) -> LLMResult:
        user = next((m.content for m in reversed(messages) if m.role == "user"), "")
        user = user.strip()

        m = re.match(r"^calc\s*:\s*(.+)$", user, flags=re.IGNORECASE)
        if m:
            action = ToolAction(tool_name="calc", tool_input={"expression": m.group(1).strip()})
            return LLMResult(raw_text=json.dumps(action.model_dump()), action=action, model=self.model_name)

        m = re.match(r"^use\s+(\w+)\s+(\{.*\})$", user, flags=re.IGNORECASE | re.DOTALL)
        if m:
            tool_name = m.group(1)
            try:
                payload = json.loads(m.group(2))
            except Exception:
                payload = {}
            action = ToolAction(tool_name=tool_name, tool_input=payload)
            return LLMResult(raw_text=json.dumps(action.model_dump()), action=action, model=self.model_name)

        # default: final
        action = FinalAction(final=f"[mock] Ho ricevuto: {user}")
        return LLMResult(raw_text=json.dumps(action.model_dump()), action=action, model=self.model_name)
