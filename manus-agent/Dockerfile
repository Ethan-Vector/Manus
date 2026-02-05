FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src
COPY evals /app/evals

RUN pip install --no-cache-dir -e .

CMD ["manus", "chat"]
