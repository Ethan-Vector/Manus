# Manus Agent

**Manus Agent** è una repo “da builder”, non un giocattolo: ti dà uno scheletro pulito per un agente LLM con
**tool use**, **stato/memory**, **guardrails** e un **mini eval harness**.  
Obiettivo: partire subito bene con una base che non si rompe alla prima demo.

> Filosofia: *niente magia*. Un agente è un **loop controllato**: osserva → decide → agisce (tool) → aggiorna stato → valuta → ripete.

---

## Cosa c’è dentro

- `src/manus_agent/` — core agentico (runner, stato, tool registry, policy)
- `tools/` — strumenti “safe-by-default” (calcolatrice, http stub)
- `guardrails/` — policy e validazione output (schema + limiti)
- `evals/` — harness + dataset smoke (regressioni veloci)
- `examples/` — demo end-to-end
- `.github/workflows/ci.yml` — CI minima (lint + test)
- `Dockerfile` — container base

---

## Quickstart (5 minuti)

### 1) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

### 2) Run (modalità mock, offline)

```bash
manus chat
```

### 3) Run un esempio “tool call”

```bash
python examples/tool_agent.py
```

---

## Come funziona (il loop)

Il runner gestisce un ciclo a passi (step):

1. Costruisce un **prompt** (messaggi + stato + tool disponibili)
2. Chiede al provider LLM un **Action** (JSON)
3. Se `tool`: esegue il tool, salva `observation` nello stato, continua
4. Se `final`: ritorna la risposta
5. Sempre: applica guardrails e limiti (max steps, timeouts, retries)

Il contratto tra modello e sistema è lo **schema Action** (vedi `manus_agent/core/schema.py`).

---

## “Production-friendly” per davvero: regole operative

- **Determinismo dove serve**: mock LLM e dataset smoke per regressioni rapide.
- **Budget di steps**: niente loop infiniti (default 6).
- **Tool registry** tipizzato: niente `eval()` o tool “aperti” a caso.
- **Guardrails**: output validato e normalizzato prima di consegnarlo al chiamante.
- **Evals**: mini-harness che ti dice subito se hai rotto il comportamento.

---

## Roadmap (se vuoi farla crescere)

- Tracing OpenTelemetry
- Tool sandboxing (subprocess isolati)
- Memory persistente (SQLite / Redis)
- RAG “pulito” con retriever e reranker modulari
- Evals con metriche (success rate / cost / latency)

---

## License

MIT — vedi `LICENSE`.
