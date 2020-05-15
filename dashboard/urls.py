from django.urls import path
from .import views


urlpatterns = [
    path('remove_task/<int:pk>', views.remove_task, name='remove_task'),
    path('remove_worker/<pk>/', views.delete_worker, name='remove-worker'),
    path('task/<pk>/', views.complete_task, name='complete_task'),
]