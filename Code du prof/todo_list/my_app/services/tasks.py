from my_app.schemas import Task
from my_app.database import database


def save_task(new_task: Task) -> Task:
    database["tasks"].append(new_task)
    return new_task


def get_all_tasks() -> list[Task]:
    tasks_data = database["tasks"]
    tasks = [Task.model_validate(data) for data in tasks_data]
    return tasks
    
