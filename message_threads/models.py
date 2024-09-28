from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=None)

    def clean(self) -> None:
        '''
        Ensure, that threads has no more than 2 participants
        '''
        if self.participants.count() > 2:
            raise ValidationError(
                'A thread cannot have more than 2 participants')

    def save(self, *args, **kwargs) -> None:
        '''
        Overriding save to ensure the clean() method called
        '''
        self.clean()
        super().save(*args, **kwargs)


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
