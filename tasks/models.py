from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title