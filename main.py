from planner import Planner
from executor import Executor
from task_repository import TaskRepository
from utils.helpers import load_config, log_info

def main():
    log_info("Starting Manus-style agent...")

    config = load_config("config/config.json")
    planner = Planner(config)
    executor = Executor(config)
    repo = TaskRepository()

    instruction = input("Enter a task instruction: ")

    plan = planner.create_plan(instruction)
    repo.save_plan(instruction, plan)
    log_info(f"Generated plan: {plan}")

    results = executor.execute_plan(plan)
    repo.save_result(instruction, results)

    log_info("Execution completed.")
    print("Final Results:", results)

if __name__ == "__main__":
    main()
