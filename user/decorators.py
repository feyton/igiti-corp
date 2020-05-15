from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from dashboard.models import NurseryManager

def staff_only(func_view):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return func_view(request, *args, **kwargs)
        return redirect('update-profile')
    return wrap

def nursery_manager(func_view):
    def wrap(request, *args, **kwargs):
        if request.user.userprofile.is_manager or request.user.is_staff:
            return func_view(request, *args, **kwargs)
        return redirect('notification')
    return wrap