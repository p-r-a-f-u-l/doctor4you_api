from django.urls import path
from . import views

urlpatterns = [
    path("locaiton/", views.Home.as_view()),
]
