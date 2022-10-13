import base64

import pyotp
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import (
    api_view,
)
from rest_framework.decorators import (
    authentication_classes,
)
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from core.otpgen import generateKey
from core.serializers import RegisterSerializer, ResetEmailPassword
from doctor4you.settings import EMAIL_HOST_USER

User = get_user_model()


class UserIndex(APIView):
    permission_classes = []

    def get(self, request):
        data = {
            "username": "",
            "profile_dp": "",
            "phone_number": "",
            "email": "",
            "password": "",
        }
        return Response(data=data)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid()
        print(serializer.error_messages)
        if serializer.errors:
            data_error = {
                "responseCode": "404",
                "responseText": "failed",
                "error": serializer.errors,
                "responseData": "Error",
                "redirect": False,
            }
            return Response(data=data_error)
        serializer.save()
        if serializer.is_valid(raise_exception=True):
            try:
                email = request.data["email"].replace(" ", "")
                Email = User.objects.get(email=email)
            except ObjectDoesNotExist:
                data_error = {
                    "responseCode": "404",
                    "responseText": "failed",
                    "error": {},
                    "responseData": "No Email Found.",
                    "redirect": False,
                }
                return Response(data=data_error)
            Email.counter += 1
            Email.save()
            keygen = generateKey()
            key = base64.b32encode(keygen.returnValue(email).encode())
            OTP = pyotp.HOTP(key)
            print(OTP.at(Email.counter))
            request.session['password'] = request.data.get("password")
            subject = "Password Reset Otp"
            msg = f"You're OTP is {OTP.at(Email.counter)}"
            send_to = email
            send_mail(subject, msg, EMAIL_HOST_USER, [send_to], fail_silently=False)

        data = {
            "responseCode": "200",
            "responseText": "success",
            "error": {},
            "responseData": "OTP SEND SUCCESSFULLY.",
            "redirect": True,
        }
        return Response(data=data)


test_param = openapi.Parameter(
    "test", openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN
)
user_response = openapi.Response("response description", ResetEmailPassword)


@swagger_auto_schema(methods=["post"], request_body=ResetEmailPassword)
@api_view(["POST", "GET"])
@authentication_classes([])
@permission_classes([])
def changepassword(request):
    if request.method == "POST":
        try:
            email = request.data["email"].replace(" ", "")
            password = request.data["password"]
            confirm_password = request.data["cnfm_password"]
            if password != confirm_password:
                raise ValidationError(
                    {
                        "responseCode": "400",
                        "responseText": "Failed",
                        "responseData": "Password MisMatch.",
                    }
                )
        except KeyError:
            data = {
                "responseCode": "400",
                "responseText": "Failed",
                "responseData": "Email Field is Required.",
            }
            return Response(data=data)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            data = {
                "responseCode": "200",
                "responseText": "Success",
                "responseData": "Password Updated.",
            }
            return Response(data=data)
        data = {
            "responseCode": "204",
            "responseText": "Failed",
            "responseData": "Email Not Found.",
        }
        return Response(data=data)
    return Response({"email": "demo.py@example.com"})


class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        token = RefreshToken(token=request.data.get("refresh"))
        token.blacklist()
        token_payload = token_backend.decode(request.data.get("refresh"))
        user = User.objects.filter(id=token_payload["user_id"])
        logout(user)
        return Response(
            {
                "message": "success",
                "code": status.HTTP_200_OK,
                "detail": "logout success",
            }
        )


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(data={"status": True}, status=status.HTTP_205_RESET_CONTENT)

#  "responseData": {
#         "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0OTAxMDk5NiwianRpIjoiY2EzM2NkYTgwYjMwNDM0ZWJkOGI3MGI2YTcyZWRlNzUiLCJ1c2VyX2lkIjoxfQ.ubVr2poiP2MhLpQ7rkCbKvhkuFUO_1ju0eBl7HDINfw",
#         "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4OTI0NTk2LCJqdGkiOiJlZGI3NzRmOGQ1NGY0N2YyYmZmYTQwODYxNWE5MWNkMCIsInVzZXJfaWQiOjF9.tH9jNMzTSKCqOnRmYBwdpUkTIOigEmn6Z4tEfaSKJlM"
#     }
