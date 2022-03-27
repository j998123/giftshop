from django.urls import path
from . import views

urlpatterns = [
    path('',views.tologin),
    path('main/', views.Login),
    path('tosign/', views.toSignup),
    path('sign/',views.Signup),
    path('admin/',views.toadmin),
    path('toadmin/',views.Delprodect),
]