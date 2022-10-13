import base64
from datetime import datetime
from django.core.mail import send_mail
from doctor4you.settings import EMAIL_HOST_USER

import pyotp
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import (
    authentication_classes,
)
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import ValidationError
from .models import User


class generateKey:
    @staticmethod
    def returnValue(phone):
        return (
            str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
        )


@authentication_classes([])
@permission_classes([])
class getEmailRegistered(APIView):
    @staticmethod
    def get(request, emailID):
        try:
            Email = User.objects.get(email=emailID)
        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    "responseCode": "404",
                    "responseText": "failed",
                    "responseData": "No Email Found.",
                    "redirect": False,
                }
            )
        Email.counter += 1
        Email.save()
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(emailID).encode())
        OTP = pyotp.HOTP(key)
        subject = "Password Reset Otp"
        msg = f"You're OTP is {OTP.at(Email.counter)}"
        send_to = emailID
        send_mail(subject, msg, EMAIL_HOST_USER, [send_to], fail_silently=False)
        data = {
            "responseCode": "200",
            "responseText": "success",
            "error": {},
            "responseData": "OTP SEND SUCCESSFULLY.",
            "redirect": True,
        }
        return Response(data=data, status=200)

    @staticmethod
    def post(request, emailID):
        try:
            Mobile = User.objects.get(email=emailID)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(emailID).encode())
        OTP = pyotp.HOTP(key)
        if OTP.verify(request.data["otp"], Mobile.counter):
            Mobile.isVerified = True
            Mobile.counter += 1
            Mobile.save()
            pyotp.HOTP(key)
            password_session = request.data["password"]
            if password_session:
                datas = {
                    User.USERNAME_FIELD: emailID,
                    "password": password_session,
                    "request": request,
                }
                user = authenticate(**datas)
                is_Login = RefreshToken.for_user(user)
                print(is_Login)
                data = {
                    "responseCode": "200",
                    "responseText": "success",
                    "responseData": "You are authorised.",
                    "token": {
                        "refresh_token": str(is_Login),
                        "access_token": str(is_Login.access_token),
                    },
                    "redirect": True,
                }
                return Response(data=data, status=200)
        data = {
            "responseCode": "400",
            "responseText": "failed",
            "responseData": "OTP EXPIRED.",
            "token": {},
            "redirect": False,
        }
        return Response(data=data, status=400)

    @staticmethod
    def put(request, emailID):
        try:
            Mobile = User.objects.get(email=emailID)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(emailID).encode())
        OTP = pyotp.HOTP(key)
        if OTP.verify(request.data["otp"], Mobile.counter):
            Mobile.isVerified = True
            Mobile.counter += 1
            Mobile.save()
            pyotp.HOTP(key)
            data = {
                "responseCode": "200",
                "responseText": "success",
                "responseData": "Success",
                "redirect": True,
            }
            return Response(data=data, status=200)
        data = {
            "responseCode": "400",
            "responseText": "failed",
            "responseData": "OTP EXPIRED.",
            "redirect": False,
        }
        return Response(data=data, status=400)
