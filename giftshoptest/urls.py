from django.urls import path
from . import views

urlpatterns = [
    path('',views.Mainpage),
    path('login/', views.tologin),
    path('tologin/', views.Login),
    path('tosign/', views.toSignup),
    path('sign/',views.Signup),
    path('personal/',views.persondetails),
    path('productlist/',views.Productlist),
    path('productlist/<int:Productid>/',views.Productdetail,name = 'Productdetail'),
    path('wishlist/<int:listid>/',views.WishList),
    path('shoppingcart/',views.Shoppingcart),
    path('payment/',views.Payment),
    path('test/', views.paymenttest, name='test'),
    path('thanks/', views.paymentsucess, name='thanks'),
    path('checkout/', views.checkout, name='checkout'),
]