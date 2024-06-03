from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dirtyfields import DirtyFieldsMixin

class ActionLog(DirtyFieldsMixin, models.Model):
    ACTION_CHOICES = [
        ('C', 'Create'),
        ('U', 'Update'),
        ('D', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=1, choices=ACTION_CHOICES)
    model = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    action_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    old_values = models.TextField(blank=True, null=True)
    new_values = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"User: {self.user.username} | Operação: {self.get_action_display()} | Registro: {self.model} {self.object_id}"
