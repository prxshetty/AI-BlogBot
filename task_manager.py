from typing import Dict, List
from task_models import Task, TaskStatus

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}

    def add_task(self, task_id: str, description: str, dependencies: List[str] = None):
        self.tasks[task_id] = Task(
            id=task_id,
            description=description,
            dependencies=dependencies or []
        )

    def get_next_tasks(self) -> List[Task]:
        ready_tasks = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                if all(self.tasks[dep].status == TaskStatus.COMPLETED for dep in task.dependencies):
                    ready_tasks.append(task)
        return ready_tasks 