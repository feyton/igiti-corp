from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .utils import validate_email


urlpatterns = [
    path('ajax/validate_email', validate_email, name='validate_email'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('admin_view/', views.admin_view, name='owner')
]