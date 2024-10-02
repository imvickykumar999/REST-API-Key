# apiapp/models.py
from django.contrib.auth.models import User
from django.db import models
import uuid

class APIKey(models.Model):
    """
    Model to store the API keys.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.key}"


class Item(models.Model):
    """
    A sample CRUD model where operations are restricted by API key.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

