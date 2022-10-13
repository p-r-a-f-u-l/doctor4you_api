from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Chat(models.Model):
    send_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sendto_User"
    )
    recieve = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="recieve_User"
    )
    msg = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.send_to)


class ChatRoom(models.Model):
    guid = models.UUIDField(default=uuid4)
    chat = models.ManyToManyField(Chat)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.guid)
