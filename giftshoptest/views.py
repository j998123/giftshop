from django.shortcuts import render

# Create your views here.

def tologin(request):
    return render(request,'login.html')