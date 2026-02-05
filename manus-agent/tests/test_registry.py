import pytest
from manus_agent.tools.registry import ToolRegistry, ToolNotFound
from manus_agent.tools.builtin.calc import CalcTool

def test_registry_register_and_run():
    reg = ToolRegistry()
    reg.register(CalcTool())
    out = reg.run("calc", {"expression": "3*3"}).output
    assert out == "9"

def test_registry_missing():
    reg = ToolRegistry()
    with pytest.raises(ToolNotFound):
        reg.run("missing", {})
