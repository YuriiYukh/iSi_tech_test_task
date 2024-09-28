from django.contrib.auth.models import User
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=None)


class Message(models.Model):
    sender = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='sent_by',
    )
    thread = models.ForeignKey(
        to=Thread,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    text = models.CharField(max_length=1024)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
