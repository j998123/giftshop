from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import re
from tkinter import messagebox
# Create your views here.

def Mainpage(request):
    return render(request,'Index.html')

def tologin(request):
    return render(request,'login.html')

def toSignup(request):
    return render(request,'Signup.html')

def Login(request):
    usn = request.GET.get("user",'')
    pas = request.GET.get("psd",'')
    if usn and pas:
        t = Customer.objects.filter(username=usn,password = pas).count()
        if t>=1:
            return HttpResponse("Login Success")
        else:
            return HttpResponse("Login Fail")
    else:
        return HttpResponse("Please enter Username and password")


def Signup(request):
    usn = request.GET.get("user",'')
    pas = request.GET.get("psd",'')
    pas2 = request.GET.get("psd2", '')
    phone = request.GET.get("pho",'')
    email = request.GET.get("ema",'')
    address = request.GET.get("add",'')
    date = request.GET.get("date",'')
    emailTrue = email.find("@") and email.endswith('.com')
    id = Customer.objects.count()+1
    if usn and pas and phone and email and address:
        try:
            Customer.objects.filter(username=usn).get()
            return HttpResponse("Username already exists")
        except:
            if pas != pas2:
                return HttpResponse("Two input password must be consistent")
            elif not emailTrue:
                return HttpResponse("Wrong email address")
            else:
                newcus = Customer(id = id,username = usn,password = pas,mobile = phone,dateofbirth = date,address = address,emailaddress=email )
                newcus.save()
                return HttpResponse("Signup success")
    else:
        return HttpResponse("Please enter all information")



def Delprodect(request):
    prod = request.GET.get("prod", '')
    try:
        Product.objects.filter(Productid=prod).get()
        Product.objects.get(Productid=prod).delete()
        return HttpResponse("Product delete")
    except:
        return HttpResponse("Product does not exist")

def addprodect(request):
    prod = request.GET.get("addprod", '')
    pron = request.GET.get("proname", '')
    prop = request.GET.get("prodinf", '')
    proi = request.GET.get("prodimage", '')
    proc = request.GET.get("prodcat", '')
    try:
        Product.objects.filter(Productid=prod).get()
        return HttpResponse("Product id already exist")
    except:
        if prod and pron and prop and proi and proc:
            newprod = Customer(Productid=prod, Productname=pron, Price=prop, category=proc, image=proi)
            newprod.save()
        return HttpResponse("Product add success")