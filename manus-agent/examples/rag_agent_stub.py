"""RAG stub.

Qui trovi SOLO il wiring “pulito” per aggiungere retrieval senza sporcare il core loop.
Scopo: ricordarti dove attaccare il retriever.

In produzione:
- implementa un retriever (es: vector db)
- aggiungi un tool 'retrieve' che ritorna top-k chunks
- fai citazioni e controlli di grounding
"""

from manus_agent.config import ManusConfig
from manus_agent.core.agent import Agent

if __name__ == "__main__":
    agent = Agent(ManusConfig(llm_provider="mock"))
    out, _ = agent.chat("use http_get_stub {"url":"https://docs"}")
    print(out)
