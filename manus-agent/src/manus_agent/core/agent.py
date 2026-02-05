from __future__ import annotations

import logging
from dataclasses import dataclass

from manus_agent.config import ManusConfig
from manus_agent.core.runner import Runner
from manus_agent.core.state import AgentState, Message
from manus_agent.guardrails.policy import OutputPolicy
from manus_agent.llm.mock import MockLLM
from manus_agent.tools.builtin.calc import CalcTool
from manus_agent.tools.builtin.http_stub import HttpStubTool
from manus_agent.tools.registry import ToolRegistry


def _build_llm(cfg: ManusConfig):
    if cfg.llm_provider == "openai":
        from manus_agent.llm.openai_provider import OpenAIChatLLM

        return OpenAIChatLLM()
    return MockLLM()


def _build_tools() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register(CalcTool())
    reg.register(HttpStubTool())
    return reg


@dataclass
class Agent:
    config: ManusConfig

    def __post_init__(self):
        logging.basicConfig(level=self.config.log_level)

        llm = _build_llm(self.config)
        tools = _build_tools()
        policy = OutputPolicy()
        self.runner = Runner(llm=llm, tools=tools, policy=policy, max_steps=self.config.max_steps)

    def chat(self, user_text: str, state: AgentState | None = None) -> tuple[str, AgentState]:
        if state is None:
            state = AgentState(messages=[Message(role="system", content="You are Manus Agent.")])

        state.add_user(user_text)
        out = self.runner.run(state)
        return out, state
