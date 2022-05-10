from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from cart.cart import Cart
from django.views import View
import stripe
from django.conf import settings
from django.urls import reverse
import uuid
import re
from tkinter import messagebox
# Create your views here.


def Mainpage(request):
    return render(request,'Index.html')

def tologin(request):
    return render(request,'login.html')

def toSignup(request):
    return render(request,'Signup.html')

stripe.api_key = settings.STRIPE_SECRET_KEY
def paymenttest(request):
    return render(request, 'testpayment.html')

def paymentsucess(request):
    return render(request, 'thanks.html')

def Payment(request):
    return render(request, 'Payment.html.')

@csrf_exempt
def persondetails(request):
    user = Customer.objects.get(id=request.session['user_id'])
    if request.POST:
        if 'Logout' in request.POST:
            request.session.flush()
            return redirect("../")
    return render(request, 'Personal_info.html', {'user':user})

def Productlist(request):
    products = Product.objects.all()
    return render(request,'Product_list.html',{'products':products})

@csrf_exempt
def Productdetail(request,Productid):
    product = Product.objects.get(Productid=Productid)
    if request.POST:
        if 'Add' in request.POST:
            add_to_cart(request,Productid,1)
            return redirect("../../shoppingcart")
    return render(request,'Product_detail.html',{'product':product})


@csrf_exempt
def WishList(request,listid):
    wishlist = Wishlist.objects.get(listid = listid)
    return render(request,'Cart_list.html',{'wishlist':wishlist})

@csrf_exempt
def Shoppingcart(request):
    if request.POST:
        if 'Remove' in request.POST:
            remove_from_cart(request,request.POST.get('Remove'))
            return redirect("../shoppingcart")
    return render(request,'Shopping_cart.html',{'cart':Cart(request)})

@csrf_exempt
def Addwishlist(request):
    return render(request,'testaddwishlist.html')

def genWishList(request):
    return render(request,'wishgen.html',)

def addwishlist(request):
    name = request.GET.get("name", '')
    date = request.GET.get("date")
    uid = str(uuid.uuid4())
    suid = ''.join(uid.split('-'))
    user = Customer.objects.get(username=request.session['user_name'])
    products = []
    for item in Cart(request):
        products.append(item.product)
    newlist = Wishlist(listid=suid, listname=name, user_id=user, deliverdate=date, address=user.address,
                       emailaddress=user.emailaddress)
    newlist.save()
    newlist.Productlist.set(products)
    request.session['newwishlist'] = suid
    return redirect("/giftshop/shoppingcart/addwishlist/genwishlist")

def Login(request):
    if request.session.get('is_login',None):
        return redirect("../")
    usn = request.GET.get("username",'')
    pas = request.GET.get("password",'')
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



def add_to_cart(request,product_id,quantity):
    product = Product.objects.get(Productid=product_id)
    price = product.Price
    cart=Cart(request)
    cart.add(product,price,quantity)

def remove_from_cart(request,product_id):
    product = Product.objects.get(Productid=product_id)
    cart=Cart(request)
    cart.remove(product)

@csrf_exempt
def checkout(request):
    for item in Cart(request):
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': item.product.stripe_price_id,
                'quantity': item.quantity,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('test')),
        )
        return JsonResponse({
            'session_id' : session.id,
            'stripe_public_key' : settings.TRIPE_PUBLISHABLE_KEY
        })



