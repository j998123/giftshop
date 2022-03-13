from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.

def tologin(request):
    return render(request,'login.html')


def Login(request):
    usn = request.GET.get("user",'')
    pas = request.GET.get("psd",'')

    if usn and pas:
        t = customerInfo.objects.filter(username=usn,password = pas).count()
        if t>=1:
            return HttpResponse("Login Success")
        else:
            return HttpResponse("Login Fail")
    else:
        return HttpResponse("Please enter Username and password")
