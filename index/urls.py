from django.contrib import admin
from django.urls import path, include
from .views import home, terms, privacy, subscribe, error

urlpatterns = [
    path('', home, name='home'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('subscribe/', subscribe, name='subscribe'),
    path('error/', error, name='error')
]