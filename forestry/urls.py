from django.urls import path

from .views import BlogPostDetailView, BlogPostListView, search, category_view


urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('<slug>', BlogPostDetailView.as_view(), name='detail'),
    path('search/', search, name='search'),
    path('category/<pk>/', category_view, name='category')
]