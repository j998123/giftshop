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
    path('productlist/<str:cat>',views.Productcatlist,name = 'Productcatlist'),
    path('productlist/<int:Productid>/',views.Productdetail,name = 'Productdetail'),
    path('wishlist/<str:listid>/',views.WishList,name='WishList'),
    path('shoppingcart/',views.Shoppingcart),
    path('shoppingcart/addwishlist',views.Addwishlist),
    path('shoppingcart/addwishlist/genwishlist',views.genWishList),
    path('shoppingcart/addwishlist/togenwishlist', views.addwishlist),
    path('payment/', views.payment,name='payment'),
    path('wishlistpayment/', views.wishlistpayment,name='wishlistpayment'),
    path('thanks/', views.paymentsucess, name='thanks'),
    path('checkout/', views.checkout, name='checkout'),
    path('ordgen/', views.GenOrder),
    path('wishordgen/', views.GenwishlistOrder),
    path('userGenOrder/', views.userGenOrder),
    path('searchcode/', views.searchcode),
    path('checkout/confirm', views.confirm),
    path('search/', views.searchproduct),
]