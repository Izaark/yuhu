from django.utils import timezone
from django.db.models import QuerySet
from typing import List
from tasks.models import Task


def get_tasks() -> QuerySet[Task]:
    return Task.objects.all()


def get_task_by_id(pk: int) -> Task:
    return Task.objects.get(pk=pk)


def delete_task_by_task(task: Task):
    task.delete()


def get_due_tasks_by_is_active(is_active=True) -> QuerySet[Task]:
    return Task.objects.filter(due_date__lt=timezone.now(), is_active=is_active)


def set_inactive_tasks():
    due_tasks = get_due_tasks_by_is_active()
    due_tasks.update(is_active=False)


def get_title_and_email_from_inactive_tasks() -> QuerySet:
    set_inactive_tasks()
    tasks = get_due_tasks_by_is_active(is_active=False)
    return tasks.values('title', 'email')
