from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from manus_agent.core.schema import FinalAction, ToolAction
from manus_agent.core.state import AgentState, TraceStep
from manus_agent.guardrails.policy import OutputPolicy
from manus_agent.llm.base import LLM
from manus_agent.tools.registry import ToolNotFound, ToolRegistry


@dataclass
class Runner:
    llm: LLM
    tools: ToolRegistry
    policy: OutputPolicy = OutputPolicy()
    max_steps: int = 6

    def run(self, state: AgentState) -> str:
        log = logging.getLogger("manus.runner")

        for step in range(self.max_steps):
            tools_list = self.tools.list()
            llm_result = self._complete_with_retry(state, tools_list)

            action = llm_result.action
            if isinstance(action, ToolAction):
                trace = TraceStep(step=step, action_type="tool", tool_name=action.tool_name, tool_input=action.tool_input)
                try:
                    out = self.tools.run(action.tool_name, action.tool_input)
                    state.add_tool_observation(action.tool_name, out.output)
                    trace.tool_output = out.output
                    state.trace.append(trace)
                    log.info("step=%s action=tool tool=%s", step, action.tool_name)
                    continue
                except ToolNotFound as e:
                    trace.error = str(e)
                    state.trace.append(trace)
                    state.add_assistant(f"Tool error: {e}")
                    return self.policy.apply(f"Tool error: {e}")
                except Exception as e:
                    trace.error = str(e)
                    state.trace.append(trace)
                    state.add_assistant(f"Tool crashed: {e}")
                    return self.policy.apply(f"Tool crashed: {e}")

            if isinstance(action, FinalAction):
                state.add_assistant(action.final)
                state.trace.append(TraceStep(step=step, action_type="final"))
                return self.policy.apply(action.final)

        # budget exhausted
        msg = "Stopped: max_steps reached. Refine the request or add a dedicated tool."
        state.add_assistant(msg)
        return self.policy.apply(msg)

    @retry(stop=stop_after_attempt(2), wait=wait_exponential_jitter(initial=0.2, max=1.2))
    def _complete_with_retry(self, state: AgentState, tools_list):
        return self.llm.complete(state.messages, tools_list)
