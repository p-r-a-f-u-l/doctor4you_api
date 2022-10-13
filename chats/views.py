from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .serializers import ChatRoomSerialzer
from .models import ChatRoom


class ChatView(ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerialzer
    http_method_names = ("get",)
