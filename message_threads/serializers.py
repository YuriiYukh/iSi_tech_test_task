from rest_framework import serializers
from django.contrib.auth.models import User

from message_threads.models import Message, Thread


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True)

    class Meta:
        model = Thread
        fields = ('id', 'participants', 'created', 'updated')

    def validate_participants(self, value):
        '''
        Ensure that there are only 2 participants in the thread
        '''
        if len(value) > 2:
            raise serializers.ValidationError(
                'A thread cannot have more than 2 participants')
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())

    class Meta:
        model = Message
        fields = ('id', 'sender', 'text', 'thread', 'created', 'is_read')
