from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied


def staff_only(func_view):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return func_view(request, *args, **kwargs)
        raise PermissionDenied
    return wrap