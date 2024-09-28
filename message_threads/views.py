from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'])
    def list_for_user(self, request):
        """
        List all threads for a given user.
        """
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, id=user_id)
        threads = Thread.objects.filter(participants=user)
        
        page = self.paginate_queryset(threads) # <- Applied pagination
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(threads, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        If a thread with the specified participants already exists, return it.
        Otherwise, create a new thread.
        """
        participants = request.data.get('participants')
        if not participants or len(participants) != 2:
            return Response({"error": "A thread must have exactly 2 participants."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if a thread with these participants already exists
        existing_thread = Thread.objects.filter(
            participants__in=participants).distinct()
        if existing_thread.exists():
            return Response(ThreadSerializer(existing_thread.first()).data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_path='thread/(?P<thread_id>\d+)/messages')
    def list_for_thread(self, request, thread_id=None):
        """
        List all messages for a given thread.
        """
        thread = get_object_or_404(Thread, id=thread_id)
        messages = Message.objects.filter(thread=thread)

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='unread-count')
    def unread_count(self, request):
        """
        Get the count of unread messages for a specific user.
        Expects the `user_id` to be passed as a query parameter.
        Example: /messages/unread-count/?user_id=1
        """
        user_id = request.query_params.get('user_id')
        user = get_object_or_404(User, id=user_id)
        unread_messages = Message.objects.filter(
            thread__participants=user, is_read=False)
        unread_count = unread_messages.count()
        return Response({'unread_count': unread_count})

    @action(detail=True, methods=['patch'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """
        Mark a message as read.
        """
        message = get_object_or_404(Message, pk=pk)
        message.is_read = True
        message.save()
        return Response(self.get_serializer(message).data)
