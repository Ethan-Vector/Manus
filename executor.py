from tool_manager import ToolManager
from utils.helpers import log_info

class Executor:
    def __init__(self, config):
        self.config = config
        self.tools = ToolManager(config)

    def execute_plan(self, plan: list):
        results = []
        for step in plan:
            action = step["action"]
            log_info(f"Executing step: {action}")
            result = self._execute_action(action)
            results.append({"step": step["step"], "result": result})
        return results

    def _execute_action(self, action: str):
        if "Analyze" in action:
            return "Instruction analyzed."
        if "Determine" in action:
            return self.tools.list_tools()
        if "Execute task" in action:
            return "Tools executed successfully."
        if "Summarize" in action:
            return "Task summary generated."
        return "Unknown action."
