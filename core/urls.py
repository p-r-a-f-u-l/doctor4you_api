from django.urls import path

from . import views, otpgen

# router = routers.SimpleRouter()
# router.register("create", views.UserIndex, basename="create")


urlpatterns = [
    path("change_password/", views.changepassword, name="email-forget"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("logoutall/", views.LogoutAllView.as_view()),
    path("user/create/", views.UserIndex.as_view(), name="create"),
    path("otpverfiy/<str:emailID>/", otpgen.getEmailRegistered.as_view(), name="otp"),
    # path("", include(router.urls)),
]
