from django.urls import path

from .views import error, home, privacy, subscribe, terms

urlpatterns = [
    path('', home, name='home'),
    path('terms/', terms, name='terms'),
    path('privacy/', privacy, name='privacy'),
    path('subscribe/igiti/corp/new/', subscribe, name='subscribe'),
    path('error/', error, name='error')
]
