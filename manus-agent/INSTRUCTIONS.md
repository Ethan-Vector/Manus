# Istruzioni operative (da leggere una volta, poi vai di build)

## Scopo della repo
Questa repo è una base pulita per un “AI Agent” con:
- loop controllato
- tool use tipizzato
- guardrails minimi
- evals smoke

È pensata per essere clonata e “riempita” con tool veri (RAG, API, workflows).

## Come la usi (workflow consigliato)

1) Parti in **mock** e fai passare evals:
```bash
pip install -e ".[dev]"
python -m manus_agent.evals.harness
```

2) Aggiungi un tool reale:
- crea `src/manus_agent/tools/builtin/<tuo_tool>.py`
- registra il tool in `_build_tools()` in `core/agent.py`
- aggiungi almeno un test in `tests/`

3) Solo dopo, collega un LLM vero (OpenAI opzionale):
```bash
pip install -e ".[openai]"
export MANUS_LLM_PROVIDER=openai
export OPENAI_API_KEY=...
manus chat
```

## Convenzioni
- Niente side-effect nei tool senza logging
- Niente secrets nel repo (usa `.env` / secret manager)
- Ogni PR deve passare: ruff + pytest + smoke evals

## Pattern “che regge”
Quando l’agente fa casino, di solito è perché:
- tool calling non è deterministico
- mancano stop conditions
- non hai test/regressioni

Questa repo ti impone struttura proprio per evitare questi classici autogol.
