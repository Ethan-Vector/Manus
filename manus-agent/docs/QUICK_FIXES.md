# Quick fixes (repo “non funziona”)

Se una repo agentica ti esplode, di solito è uno di questi:

1) **Dipendenze non pin-ate / ambienti sporchi**
- Soluzione: venv pulito + `pip install -e ".[dev]"`

2) **Contratto tool calling ambiguo**
- Soluzione: schema JSON stretto (Action) e parser robusto.

3) **Loop senza stop conditions**
- Soluzione: `max_steps` e stop per ripetizione/errore.

4) **Tool che non valida input**
- Soluzione: pydantic su input tool + errori “puliti” verso LLM.

5) **Nessun test**
- Soluzione: smoke dataset + unit test per tool registry e policy.

Questa repo nasce esattamente per evitare questi problemi.
