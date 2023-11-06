from django.urls import path
from tasks.views import TaskListCreateAPIView ,TaskDetailUpdateDestroyAPIView

urlpatterns = [
    path('tasks', TaskListCreateAPIView.as_view(), name='task-create-list'),
    path('tasks/<int:pk>', TaskDetailUpdateDestroyAPIView.as_view(), name='task-detail-update-destroy'),
]
