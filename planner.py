from utils.helpers import log_info

class Planner:
    def __init__(self, config):
        self.config = config

    def create_plan(self, instruction: str):
        log_info(f"Planning for instruction: {instruction}")
        plan = [
            {"step": 1, "action": "Analyze instruction"},
            {"step": 2, "action": "Determine required tools"},
            {"step": 3, "action": "Execute task using tools"},
            {"step": 4, "action": "Summarize the output"},
        ]
        return plan
