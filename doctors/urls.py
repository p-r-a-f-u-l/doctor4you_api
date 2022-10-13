from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register("doctor", views.DoctorIndex),
router.register("topdoctor", views.TopDoctorView),
router.register("specialization", views.DoctorListView),
router.register("rating", views.DoctorRateView),
router.register("doctornearby", views.DoctorNearByIndex)

urlpatterns = [
    path("doctor/<int:pk>/", views.DoctorIndexID.as_view(), name="doctor_index"),
    path("doctor/<int:pk>/review/", views.DoctorAddRate.as_view(), name="doctor_rate"),
    path("fav/", views.FavIndexID.as_view(), name="fav_here"),
    path("", include(router.urls)),
]
