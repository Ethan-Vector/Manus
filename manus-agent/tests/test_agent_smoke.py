from manus_agent.config import ManusConfig
from manus_agent.core.agent import Agent

def test_agent_smoke():
    agent = Agent(ManusConfig(llm_provider="mock", max_steps=4))
    out, _ = agent.chat("calc: 1+1")
    assert "2" in out
