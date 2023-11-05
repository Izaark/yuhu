from typing import List
from tasks.models import Task


def get_tasks() -> List[Task]:
    return Task.objects.all()


def get_task_by_id(pk: int) -> Task:
    return Task.objects.get(pk=pk)


def delete_task_by_task(task: Task):
    task.delete()