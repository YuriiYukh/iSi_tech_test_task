from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from message_threads.views import ThreadViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'threads', ThreadViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
