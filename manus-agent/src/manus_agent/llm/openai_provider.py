from __future__ import annotations

import json
from dataclasses import dataclass
from os import getenv
from typing import Dict, List

from manus_agent.core.schema import FinalAction, LLMResult, ToolAction
from manus_agent.core.state import Message
from manus_agent.llm.base import LLM


@dataclass
class OpenAIChatLLM(LLM):
    """Provider OpenAI opzionale.

    Nota pratica: in questa template NON forziamo tool-calling “vendor specific”.
    Usiamo invece un prompt che chiede al modello di restituire l'Action schema in JSON.
    È più portabile e più facile da testare.

    Per usarlo:
    - pip install -e ".[openai]"
    - set OPENAI_API_KEY
    - set MANUS_LLM_PROVIDER=openai
    """

    model: str = getenv("OPENAI_MODEL", "gpt-4.1-mini")

    def complete(self, messages: List[Message], tools: List[Dict[str, str]]) -> LLMResult:
        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError("OpenAI dependency missing. Install extras: pip install -e ".[openai]"") from e

        client = OpenAI()

        tool_lines = "\n".join([f"- {t['name']}: {t['description']}" for t in tools])
        system = (
            "You are Manus Agent. You MUST reply with a single JSON object matching one of these schemas:\n"
            "1) {"type":"tool","tool_name":"...","tool_input":{...}}\n"
            "2) {"type":"final","final":"..."}\n"
            "Available tools:\n"
            f"{tool_lines}\n"
            "If a tool is needed, choose type=tool. Otherwise choose type=final."
        )

        chat = [{"role": "system", "content": system}]
        for m in messages:
            if m.role == "tool":
                chat.append({"role": "assistant", "content": f"Tool [{m.name}] returned: {m.content}"})
            else:
                chat.append({"role": m.role, "content": m.content})

        resp = client.chat.completions.create(
            model=self.model,
            messages=chat,
            temperature=0.2,
        )

        text = resp.choices[0].message.content or ""
        text = text.strip()

        # Robust parse: if the model wraps JSON in markdown, extract it.
        json_str = text
        if "```" in text:
            json_str = text.split("```")[-2].strip() if len(text.split("```")) >= 3 else text

        try:
            data = json.loads(json_str)
        except Exception:
            action = FinalAction(final=text)
            return LLMResult(raw_text=text, action=action, model=self.model)

        if data.get("type") == "tool":
            action = ToolAction(tool_name=data.get("tool_name", ""), tool_input=data.get("tool_input", {}) or {})
        else:
            action = FinalAction(final=str(data.get("final", "")) or text)

        return LLMResult(raw_text=text, action=action, model=self.model)
