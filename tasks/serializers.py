from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    email = serializers.EmailField()
    description = serializers.CharField()
    class Meta:
        model = Task
        fields = ('id', 'title', 'email', 'description')
