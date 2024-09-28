from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer



class ThreadViewSet(viewsets.ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination # <- example - /threads/list_for_user/?user_id=1&limit=5&offset=0
    
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_for_user(self, request):
        """
        Retrieve all threads for a specific user.
        URL Validation: Ensure that the user_id is provided and valid.
        Example: /threads/list_for_user/?user_id=1
        """
        user_id = request.query_params.get('user_id')

        # Validate that user_id is provided and is an integer (url validation)
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "user_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        threads = Thread.objects.filter(participants=user)

        page = self.paginate_queryset(threads)  # <- Applied pagination
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(threads, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new thread, or return an existing one if the same participants already exist.
        URL Validation: Validate that participants array contains exactly 2 participants.
        """
        participants = request.data.get('participants')
        if not participants or len(participants) != 2:
            return Response({"error": "A thread must have exactly 2 participants."},
                            status=status.HTTP_400_BAD_REQUEST)

        for participant_id in participants:
            try:
                int(participant_id)
            except ValueError:
                return Response({"error": f"Invalid participant ID: {participant_id}"}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure each participant exists in the database
            user = get_object_or_404(User, id=participant_id)

        # Check if a thread with these participants already exists
        existing_thread = Thread.objects.filter(
            participants__in=participants).distinct()
        if existing_thread.exists():
            return Response(ThreadSerializer(existing_thread.first()).data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination # <- example: /messages/?limit=5&offset=0
    
    authentication_classes = [JWTAuthentication]  # Use JWT authentication
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='thread/(?P<thread_id>\d+)/messages')
    def list_for_thread(self, request, thread_id=None):
        """
        List all messages for a specific thread.
        URL Validation: Ensure that thread_id is valid.
        Example: /messages/thread/1/messages/
        """
        # Validate that thread_id is a valid integer and exists in the database
        try:
            thread_id = int(thread_id)
        except ValueError:
            return Response({"error": "thread_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

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
        Retrieve the count of unread messages for a specific user.
        URL Validation: Ensure user_id is valid.
        Example: /messages/unread-count/?user_id=1
        """
        user_id = request.query_params.get('user_id')
        
        # Validate that user_id is provided and is an integer
        if not user_id:
            return Response({"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "user_id must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=user_id)
        unread_messages = Message.objects.filter(
            thread__participants=user, is_read=False)
        unread_count = unread_messages.count()
        return Response({'unread_count': unread_count})

    @action(detail=True, methods=['patch'], url_path='mark-as-read')
    def mark_as_read(self, request, pk=None):
        """
        Mark a message as read.
        URL Validation: Ensure that the message ID (pk) is valid.
        Example: /messages/1/mark-as-read/
        """
        # Validate that the message ID (pk) exists
        message = get_object_or_404(Message, pk=pk)
        message.is_read = True
        message.save()
        return Response(self.get_serializer(message).data)
