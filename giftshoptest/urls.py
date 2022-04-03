from django.urls import path
from . import views

urlpatterns = [
    path('',views.Mainpage),
    path('login/', views.tologin),
    path('tologin/', views.Login),
    path('tosign/', views.toSignup),
    path('sign/',views.Signup),
    path('admin/',views.toadmin),
    path('toadmin/',views.Delprodect),
]