from django.urls import path
from . import views

urlpatterns = [
    path('',views.tologin),
    path('main/',views.Login),
]