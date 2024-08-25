from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AbstractUser

from django.contrib import messages
from panel.decoratos import user_authenticated, user_not_authenticated
from .forms import RegisterForm, LoginForm

# Create your views here.


@user_not_authenticated
def login_view(request: HttpRequest):
    if request.method == 'POST':
        login_form = LoginForm(request=request, data=request.POST)
        if login_form.is_valid():

            username: str = login_form.cleaned_data.get('username', '')
            password: str = login_form.cleaned_data.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('panel:home-view')
                else:
                    messages.error(
                        request, "You don't have permission to login")
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Something went wrong. Please try again')
    login_form = LoginForm()
    return render(request, 'users/login.html', {'login_form': login_form, 'login': True, 'register': False})


@user_authenticated
def logout_view(request: HttpRequest):
    logout(request)
    return redirect('users:login-view')


@user_not_authenticated
def register_view(request: HttpRequest):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user: AbstractUser = register_form.save(commit=False)
            user.save()
            messages.success(
                request, 'Your account was created. You can now login')
            return redirect('users:login-view')
        else:
            for message in register_form.error_messages.values():
                messages.error(request, message)

    register_form = RegisterForm()
    return render(request, 'users/register.html', {'register_form': register_form, 'login': False, 'register': True})
