from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import re
from tkinter import messagebox
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

def toSignup(request):
    return render(request,'Signup.html')

def Signup(request):
    usn = request.GET.get("user",'')
    pas = request.GET.get("psd",'')
    pas2 = request.GET.get("psd2", '')
    phone = request.GET.get("pho",'')
    email = request.GET.get("ema",'')
    address = request.GET.get("add",'')
    emailTrue = email.find("@") and email.endswith('.com')

    if usn and pas and phone and email and address:
        if pas != pas2:
            return HttpResponse("Two input password must be consistent")
        elif not emailTrue:
            return HttpResponse("Wrong email address")
        elif not re.match(r'^1[3-9]\d{9}$', phone):
            return HttpResponse("Please enter vaild phone number")
        else:
            newcus = customerInfo(id = 11,username = usn,password = pas,mobile = phone,dateofbirth = null,address = address )
            newcus.save()
            return HttpResponse("Signup success")
    else:
        return HttpResponse("Please enter all information")
