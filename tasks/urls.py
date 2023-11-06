from django.urls import path
from tasks.views import (TaskListCreateAPIView,
                         TaskDetailUpdateDestroyAPIView,
                         create_task,
                         task_list_view,
                         task_update,
                         delete_task,
                         )

urlpatterns = [
    path('tasks', TaskListCreateAPIView.as_view(), name='task-create-list'),
    path('tasks/<int:pk>', TaskDetailUpdateDestroyAPIView.as_view(), name='task-detail-update-destroy'),
    path('tasks/create', create_task, name='create_task_url'),
    path('tasks/list', task_list_view, name='list_task_url'),
    path('tasks/update/<int:task_id>/', task_update, name='task_update'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),

]
