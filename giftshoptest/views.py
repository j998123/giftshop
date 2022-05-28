from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import *
from cart.cart import Cart
import stripe
from django.conf import settings
from django.urls import reverse
from datetime import datetime
import uuid
# Create your views here.


def Mainpage(request):
    return render(request,'Index.html')

def tologin(request):
    return render(request,'login.html')

def toSignup(request):
    return render(request,'Signup.html')

stripe.api_key = settings.STRIPE_SECRET_KEY
def payment(request):
    user = []
    if request.session.get('user_id',None):
        user = Customer.objects.get(id=request.session['user_id'])
    else:
        user = []
    return render(request, 'Check_out.html',{'cart':Cart(request),'user':user,})

def wishlistpayment(request):
    wishlist = Wishlist.objects.get(listid=request.session['paywishlist'])
    user = wishlist.user_id
    return render(request, 'Invitee_checkout.html',{'cart':Cart(request),'user':user})

def paymentsucess(request):
    return render(request, 'thanks.html')

@csrf_exempt
def persondetails(request):
    user = Customer.objects.get(id=request.session['user_id'])
    wishlists = Wishlist.objects.all()
    list = {}
    for wishlist in wishlists:
        name = wishlist.listname
        products = wishlist.Productlist.all()
        list[name] = products
    if request.POST:
        if 'Logout' in request.POST:
            request.session.flush()
            return redirect("../")
    return render(request, 'Personal_info.html', {'user':user,'wishlists':wishlists,'lists':list,})

def Productlist(request):
    products = Product.objects.all()
    return render(request,'Product_list.html',{'products':products})

def Productcatlist(request,cat):
    catProducts = Product.objects.filter(category__icontains=cat)
    return render(request,'Product_catlist.html',{'products':catProducts})

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
    wishlist = Wishlist.objects.get(listid=listid)
    if request.POST:
        if 'Add' in request.POST:
            add_to_cart(request,request.POST.get('Add'),1)
            return redirect("/giftshop/wishlist/"+listid)
        if 'Remove' in request.POST:
            try:
             remove_from_cart(request, request.POST.get('Remove'))
            except:
                return redirect("/giftshop/wishlist/" + listid)
            return redirect("/giftshop/wishlist/" + listid)
        if 'Check' in request.POST:
            request.session['paywishlist'] = listid
            request.session['userwishlist'] = wishlist.user_id.id
            return redirect("/giftshop/wishlistpayment/")
    return render(request,'Pay_Cart.html',{'wishlist':wishlist,'cart':Cart(request)})


@csrf_exempt
def Shoppingcart(request):
    if request.POST:
        if 'Remove' in request.POST:
            remove_from_cart(request,request.POST.get('Remove'))
            return redirect("../shoppingcart")
        if 'Gen' in request.POST:
            if request.session.get('is_login', None):
                return redirect("../shoppingcart/addwishlist")
            else:
                return redirect("../login")
    return render(request,'Shopping_cart.html',{'cart':Cart(request)})

@csrf_exempt
def Addwishlist(request):
    return render(request,'Gen_WishList.html')


def genWishList(request):
    wish = Wishlist.objects.get(listid = request.session['newwishlist'])
    return render(request,'Generate.html', {'wish':wish})

def confirm(request):
    order = Order.objects.get(Orderid= request.session['neworder'])
    return render(request,'checkouconfirm.html', {'cart':Cart(request),'order':order})

def addwishlist(request):
    name = request.GET.get("name", '')
    date = request.GET.get("date")
    suid = str(uuid.uuid4().int)[-6:]
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


def searchcode(request):
    code = request.GET.get("code",'')
    if code:
        try:
            wishlist = Wishlist.objects.get(listid=code)
        except:
            messages.error(request, 'wishlist is not exist')
            return redirect("/giftshop")
        wishlist = Wishlist.objects.get(listid=code)
        return redirect('WishList', listid=wishlist.listid)
    else:
        messages.error(request, 'Please enter a event code')
        return redirect("/giftshop")

def searchproduct(request):
    prod = request.GET.get("prod",'')
    if prod:
        try:
            Products = Product.objects.filter(Productname__contains=prod)
        except:
            messages.error(request, 'Product is not exist')
            return redirect("/giftshop")
        return render(request,'Search_Product_list.html',{'products':Products})
    else:
        messages.error(request, 'Please enter something')
        return redirect("/giftshop")

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
    items = []
    for item in Cart(request):
        items.append({
            'price': item.product.stripe_price_id,
            'quantity': item.quantity,
        })
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('payment')),
    )
    if request.session['paywishlist'] !=None:
        wishlist = Wishlist.objects.get(listid=request.session['paywishlist'])
        for item in Cart(request):
            Product = item.product
            wishlist.Productlist.remove(Product)
    Cart(request).clear()
    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.TRIPE_PUBLISHABLE_KEY
    })

def userGenOrder(request):
    productlist = []
    for item in Cart(request):
        productlist.append(item.product)
    oid = str(uuid.uuid4().int)[-12:]
    user = Customer.objects.get(id=request.session['user_id'])
    neworder = Order(Orderid=oid, customername=user.Name, Price=Cart(request).summary(), mobile=user.mobile, deliverdate=datetime.today(),
                     address=user.address, emailaddress=user.emailaddress, status=2)
    neworder.save()
    neworder.Productlist.set(productlist)
    request.session['neworder'] = oid
    return redirect("/giftshop/checkout/confirm")


def GenOrder(request):
    name = request.GET.get("Frist", '')+request.GET.get("Last",'')
    email = request.GET.get("Email" )
    mobile = request.GET.get("Mobile")
    address = request.GET.get("Address")
    oid = str(uuid.uuid4().int)[-12:]
    date = datetime.today()
    productlist=[]
    for item in Cart(request):
        productlist.append(item.product)
    neworder = Order(Orderid=oid,customername=name,Price=Cart(request).summary(),mobile=mobile,deliverdate=date,address=address,emailaddress=email,status=1)
    neworder.save()
    neworder.Productlist.set(productlist)
    request.session['neworder'] = oid
    return redirect("/giftshop/checkout/confirm")

def GenwishlistOrder(request):
    name = request.GET.get("name", '')
    user = Customer.objects.get(id=request.session['userwishlist'])
    wishlist = Wishlist.objects.get(listid=request.session['paywishlist'])
    if name:
        oid = str(uuid.uuid4().int)[-12:]
        date = wishlist.deliverdate
        address = wishlist.address
        mobile = user.mobile
        email = user.emailaddress
        productlist=[]
        for item in Cart(request):
            productlist.append(item.product)
        neworder = Order(Orderid=oid,customername=name,Price=Cart(request).summary(),mobile=mobile,deliverdate=date,address=address,emailaddress=email,status=1)
        neworder.save()
        neworder.Productlist.set(productlist)
        request.session['neworder'] = oid
    else:
        messages.error(request, 'Please enter your name')
        return redirect("/giftshop/wishlistpayment/")
    return redirect("/giftshop/checkout/confirm")
