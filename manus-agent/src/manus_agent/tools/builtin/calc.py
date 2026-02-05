from __future__ import annotations

import ast
import operator as op
from dataclasses import dataclass
from typing import Any, Dict

from manus_agent.tools.base import Tool, ToolResult


_ALLOWED = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node):
    if isinstance(node, ast.Num):  # py<3.8
        return node.n
    if isinstance(node, ast.Constant):  # py>=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers are allowed.")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
        return _ALLOWED[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression.")


@dataclass
class CalcTool(Tool):
    name: str = "calc"
    description: str = "Evaluate a basic arithmetic expression safely. Input: {"expression": "2*(3+4)"}"

    def run(self, tool_input: Dict[str, Any]) -> ToolResult:
        expr = str(tool_input.get("expression", "")).strip()
        if not expr:
            return ToolResult(output="Error: missing 'expression'.")
        try:
            tree = ast.parse(expr, mode="eval")
            value = _eval(tree.body)
            return ToolResult(output=str(value))
        except Exception as e:
            return ToolResult(output=f"Error: {e}")
