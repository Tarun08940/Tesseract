from django.db import models
from django.conf import settings

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
from django.conf import settings