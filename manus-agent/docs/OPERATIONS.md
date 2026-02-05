# Operazioni (logging, sicurezza, affidabilità)

## Logging
Il runner logga:
- step index
- action type
- tool invocato
- errori e retry

In produzione: log JSON + correlazione (request_id).

## Timeouts e retry
- I tools vanno trattati come dipendenze esterne (possono fallire).
- Usa timeouts brevi e retry con backoff (tenacity).

## Tool safety
Regola semplice: **tool = codice con privilegi**.
- allowlist stretta
- input validation
- niente tool “shell” senza sandbox
- niente accesso a secrets se non necessario

## Guardrails
- max steps
- max output length
- schema validation stretta
- blocco di tool non autorizzati

## Evals
Prima di fare merge:
- `pytest`
- `python -m manus_agent.evals.harness`

Se gli smoke test falliscono, non deployare. Fine.

