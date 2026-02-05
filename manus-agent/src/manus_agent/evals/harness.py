from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

from manus_agent.config import ManusConfig
from manus_agent.core.agent import Agent
from manus_agent.core.state import AgentState, Message


@dataclass
class EvalCase:
    id: str
    input: str
    must_contain: str


def load_cases(path: Path) -> List[EvalCase]:
    cases: List[EvalCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        cases.append(EvalCase(id=obj["id"], input=obj["input"], must_contain=obj["must_contain"]))
    return cases


def run_smoke(dataset_path: str = "evals/datasets/smoke.jsonl") -> int:
    cfg = ManusConfig(llm_provider="mock", max_steps=4, log_level="WARNING")
    agent = Agent(cfg)
    state = AgentState(messages=[Message(role="system", content="You are Manus Agent.")])

    cases = load_cases(Path(dataset_path))
    failures = 0

    for c in cases:
        out, state = agent.chat(c.input, state)
        if c.must_contain not in out:
            failures += 1
            print(f"[FAIL] {c.id} expected contains={c.must_contain!r} got={out!r}")
        else:
            print(f"[PASS] {c.id}")

    return failures


if __name__ == "__main__":
    raise SystemExit(run_smoke())
