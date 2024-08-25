from django.shortcuts import redirect
from django.http import HttpRequest
from functools import wraps


def user_not_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return wrapper_func
    if function:
        return decorator(function)
    return decorator


def user_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            return redirect(redirect_url)
        return wrapper_func
    if function:
        return decorator(function)
    return decorator
