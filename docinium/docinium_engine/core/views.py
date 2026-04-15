from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def containers(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to view containers.')
        return redirect('login')
    return render(request, 'core/containers.html')

def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            messages.info(request, 'Please enter both username and password.')
            return render(request, 'accounts/login.html')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome to datan, dear {username}!')
            return redirect('/', username=username)
        else:
            messages.info(
                request, 'Login failed. Please check your username/password.')
    return render(request, 'accounts/login.html')


def Logout(request):
    logout(request)
    messages.success(
        request, f'logged out successfully !!')
    return redirect('/')