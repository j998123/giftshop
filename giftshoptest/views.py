from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from .models import *
from cart.cart import Cart
import re
from tkinter import messagebox
# Create your views here.

def Mainpage(request):
    return render(request,'Index.html')

def tologin(request):
    return render(request,'login.html')

def toSignup(request):
    return render(request,'Signup.html')

def persondetails(request):
    return render(request,'Personal_info.html')

def Productlist(request):
    return render(request,'Product_list.html')

def Productdetail(request):
    return render(request,'Product_detail.html')

def Shoppingcart(request):
    return render(request,'Shopping_cart.html')

def Login(request):
    # if request.session.get('is_login',None):
    #     return redirect("../")
    usn = request.GET.get("user",'')
    pas = request.GET.get("psd",'')
    if usn and pas:
        try:
            user = Customer.objects.get(username=usn)
        except:
            messages.error(request,'User does not exist')
            return redirect("../login")
        if user.password == pas:
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.username
            return redirect("../")
        else:
            messages.error(request, 'The password is incorrect')
            return redirect("../login")
    else:
        messages.error(request, 'Please enter username and password')
        return redirect("../login")


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
            messages.error(request, 'Username already exists')
            return redirect("../tosign")
        except:
            if pas != pas2:
                messages.error(request, 'Two input password must be consistent')
                return redirect("../tosign")
            elif not emailTrue:
                messages.error(request, 'Wrong email address')
                return redirect("../tosign")
            else:
                newcus = Customer(id = id,username = usn,password = pas,mobile = phone,dateofbirth = date,address = address,emailaddress=email )
                newcus.save()
                messages.error(request, 'Signup success')
                return redirect("../login")
    else:
        messages.error(request, 'Please enter all information')
        return redirect("../tosign")



