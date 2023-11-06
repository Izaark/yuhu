from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from tasks.serializers import TaskSerializer
from tasks.providers import get_tasks, delete_task_by_task, get_task_by_id
from tasks.lib.exceptions import get_object_by_id, get_task_and_paginator_by_tasks_and_page
from tasks.lib.utils import create_notification_email
from tasks.lib.constants import NOTIFICATION_ACTION_CREATE, NOTIFICATION_ACTION_UPDATE

class TaskListCreateAPIView(APIView):

    permission_classes = [permissions.AllowAny]
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
    authentication_classes = [TokenAuthentication]
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
