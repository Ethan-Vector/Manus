import json
import os
from utils.helpers import log_info

class TaskRepository:
    def __init__(self, storage_path="logs/tasks.jsonl"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    def save_plan(self, instruction: str, plan: list):
        log_info("Saving plan...")
        self._write_entry({"instruction": instruction, "plan": plan})

    def save_result(self, instruction: str, result: list):
        log_info("Saving results...")
        self._write_entry({"instruction": instruction, "results": result})

    def _write_entry(self, data: dict):
        with open(self.storage_path, "a") as f:
            f.write(json.dumps(data) + "\n")
