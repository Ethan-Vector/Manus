# Contributing

## Dev setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Checks
```bash
ruff check .
pytest
python -m manus_agent.evals.harness
```

## PR rules (semplici)
- Se tocchi tools o policy, aggiungi almeno 1 test.
- Se cambi comportamento conversazionale, aggiorna smoke dataset.
