from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("chat", views.ChatView)

urlpatterns = [
    path("", include(router.urls)),
]
