from django.db.models import QuerySet
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from tasks.models import Task
from tasks.providers import get_task_by_id


def get_object_by_id(pk: int):
    try:
        return get_task_by_id(pk)
    except Task.DoesNotExist:
        raise Http404


def get_task_and_paginator_by_tasks_and_page(tasks: QuerySet[Task], page: int) -> (Paginator.page, Paginator):
    paginator = Paginator(tasks, 5)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    return tasks, paginator
