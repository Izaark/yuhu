from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    email = serializers.EmailField()
    description = serializers.CharField()
    due_date = serializers.DateTimeField(allow_null=True)
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'email', 'description', 'due_date', 'is_active')
