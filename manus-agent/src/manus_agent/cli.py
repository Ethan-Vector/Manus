from __future__ import annotations

import argparse
from rich.console import Console
from rich.panel import Panel

from manus_agent.config import ManusConfig
from manus_agent.core.agent import Agent
from manus_agent.core.state import AgentState, Message


def chat_loop() -> int:
    console = Console()
    cfg = ManusConfig.from_env()
    agent = Agent(cfg)
    state = AgentState(messages=[Message(role="system", content="You are Manus Agent.")])

    console.print(Panel.fit("Manus Agent (type 'exit' to quit)"))
    while True:
        user = console.input("[bold]you[/bold]> ").strip()
        if user.lower() in {"exit", "quit"}:
            break
        out, state = agent.chat(user, state)
        console.print(f"[bold]manus[/bold]> {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="manus")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("chat", help="Interactive chat loop (mock by default).")

    args = parser.parse_args()
    if args.cmd == "chat":
        return chat_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
