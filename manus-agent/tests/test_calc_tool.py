from manus_agent.tools.builtin.calc import CalcTool

def test_calc_tool_basic():
    tool = CalcTool()
    out = tool.run({"expression": "2+2"}).output
    assert out == "4"
