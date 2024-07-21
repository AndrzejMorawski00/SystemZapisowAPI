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


def permission_based_access(function=None, redirect_url="/", groups=None):
    if groups is None:
        groups = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                is_admin = request.user.is_staff or request.user.is_superuser #type:ignore
                has_group = request.user.groups.filter(name__in=groups).exists() #type:ignore
                if is_admin or has_group:
                    return view_func(request, *args, **kwargs)
            return redirect(redirect_url)
        return wrapped_func

    if function:
        return decorator(function)
    return decorator


