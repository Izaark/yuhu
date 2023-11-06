import requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from tasks.serializers import TaskSerializer
from tasks.providers import get_tasks, delete_task_by_task, get_task_by_id
from tasks.lib.exceptions import get_object_by_id, get_task_and_paginator_by_tasks_and_page
from tasks.lib.utils import create_notification_email
from tasks.forms import TaskForm, TaskUpdateForm
from tasks.lib.constants import NOTIFICATION_ACTION_CREATE, NOTIFICATION_ACTION_UPDATE, LOCAL_SERVER, USER_AUTH_TOKEN


class TaskListCreateAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        tasks = get_tasks()
        page = request.query_params.get('page')
        tasks, paginator = get_task_and_paginator_by_tasks_and_page(tasks=tasks, page=page)
        serializer = TaskSerializer(tasks, many=True)
        return Response({
            'total': paginator.count,
            'page': int(page) if page else 1,
            'pages': paginator.num_pages,
            'results': serializer.data
        })


    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            task = get_task_by_id(pk=serializer.data.get("id"))
            create_notification_email(title=task.title, email=task.email, action=NOTIFICATION_ACTION_CREATE)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailUpdateDestroyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        task = get_object_by_id(pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_by_id(pk=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_notification_email(title=task.title, email=task.email, action=NOTIFICATION_ACTION_UPDATE)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        task = get_object_by_id(pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            create_notification_email(title=task.title, email=task.email, action=NOTIFICATION_ACTION_UPDATE)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_by_id(pk=pk)
        delete_task_by_task(task=task)
        return Response(status=status.HTTP_204_NO_CONTENT)


def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            email = form.cleaned_data.get('email')
            create_notification_email(title=title, email=email, action=NOTIFICATION_ACTION_CREATE)
            form.save()
            return HttpResponseRedirect('list')
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})


def task_list_view(request):
    page = request.GET.get('page', 1)
    response = requests.get(
        f'{LOCAL_SERVER}?page={page}',
        headers= {"Authorization": f"Token {USER_AUTH_TOKEN}"}
    )
    if response.status_code == 200:
        tasks = response.json()
    else:
        tasks = {}

    return render(request, 'tasks_list.html', {'tasks': tasks})


def task_update(request, task_id):
    task = get_object_by_id(pk=task_id)

    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            create_notification_email(title=task.title, email=task.email, action=NOTIFICATION_ACTION_UPDATE)
            form.save()
            return JsonResponse({"message": "Task updated successfully."}, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = TaskUpdateForm(instance=task)
    return render(request, 'update_task.html', {'form': form, 'task_id': task.id})


@require_POST
def delete_task(request, task_id):
    if request.POST.get('_method') == 'DELETE':
        task = get_object_by_id(pk=task_id)
        delete_task_by_task(task=task)
        return redirect('list_task_url')