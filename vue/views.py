from django.shortcuts import render

def login(request):
    return render(request,'vue/login_register.html')

def homeFeed(request):
    return render(request,'vue/home.html')




