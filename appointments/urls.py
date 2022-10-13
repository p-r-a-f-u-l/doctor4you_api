from rest_framework import routers
from django.urls import include, path

from . import views

router = routers.SimpleRouter()
router.register("appoint", views.AppointmentView, basename="appoint")
router.register("patient", views.PatientView, basename="patient")
router.register("fee", views.FeeView, basename="fee")
router.register("upcoming", views.UpcomingAppointView, basename="upcoming")
router.register("pastseh", views.PastAppointView, basename="pastsch")

urlpatterns = [
    path(
        "upcoming/<int:pk>/review/",
        views.DoctorReviewView.as_view(),
        name="upcoming review",
    ),
    path(
        "pastseh/<int:pk>/review/",
        views.DoctorReviewView.as_view(),
        name="upcoming review",
    ),
    path("", include(router.urls)),
]
