# Architettura

Qui ti spiego la repo come la leggerei io quando devo metterci mano in produzione.

## Moduli chiave

### 1) Core loop
- `core/runner.py` governa i passi dell’agente (max steps, stop conditions).
- `core/agent.py` è una facciata “comoda”: prende input utente e ritorna output.
- `core/state.py` gestisce memoria conversazionale + trace delle azioni.

### 2) Contratto LLM ↔ sistema
Il modello NON decide “liberamente” cosa fare. Deve restituire un oggetto `Action`:

- `type`: `"tool"` o `"final"`
- se `"tool"`: `tool_name` + `tool_input`
- se `"final"`: `final`

Questo riduce l’ambiguità e ti rende più facile fare:
- logging strutturato
- debugging
- evals

### 3) Tools
- `tools/base.py` definisce l’interfaccia.
- `tools/registry.py` è il catalogo. Qui puoi imporre allowlist, timeouts, ecc.
- `tools/builtin/*` sono esempi (calc, http stub).

### 4) Guardrails
- `guardrails/policy.py` impone vincoli: max length, blocchi, normalizzazione.
- In produzione metteresti qui: PII redaction, compliance, content filters, ecc.

### 5) Evals
- `evals/harness.py` esegue scenari e controlla pass/fail.
- `evals/datasets/smoke.jsonl` è un set minimo per non spaccare tutto.

## Estensioni consigliate (ordine pratico)

1. Aggiungi un tool “reale” (es: search interno) e testalo.
2. Inserisci persistence dello stato (SQLite).
3. Aggiungi tracing e metriche (latency/cost).
4. Allarga evals con casi edge e regressioni.

