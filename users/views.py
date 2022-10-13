from django.shortcuts import render
from django.http import HttpResponse


def setsession(request):
    request.session["sname"] = "bittu"
    request.session["semail"] = "bittu.sssit@gmail.com"
    return HttpResponse("session is set")


def getsession(request):
    studentname = request.session["sname"]
    studentemail = request.session["semail"]
    return HttpResponse(studentname + " " + studentemail)
