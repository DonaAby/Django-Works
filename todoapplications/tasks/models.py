from django.db import models

class Todo(models.Model):
    task_name=models.CharField(max_length=200)
    user=models.CharField(max_length=230)
    status=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.task_name
