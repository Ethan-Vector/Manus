from manus_agent.config import ManusConfig
from manus_agent.core.agent import Agent

if __name__ == "__main__":
    agent = Agent(ManusConfig(llm_provider="mock"))
    out, _ = agent.chat("hello")
    print(out)
