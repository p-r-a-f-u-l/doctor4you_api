from .models import ChatRoom, Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"


class ChatRoomSerialzer(serializers.ModelSerializer):
    chat = ChatSerializer(many=True)
    chatbtw = serializers.SerializerMethodField(read_only=True)

    def get_chatbtw(self, chatroom: ChatRoom):
        return chatroom.chat.send_to.username, chatroom.chat.recieve.username

    class Meta:
        model = ChatRoom
        fields = "__all__"
