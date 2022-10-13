from django.urls import path, include

from . import views

urlpatterns = [
    path("ssession", views.setsession),
    path("gsession", views.getsession),
]
