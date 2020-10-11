from os import name

from django.urls import path

from .views import (BlogPostDetailView, BlogPostListView, CommentReplyView,
                    add_comment, category_view, search)

urlpatterns = [
    path('', BlogPostListView.as_view(), name='list'),
    path('<slug>', BlogPostDetailView.as_view(), name='detail'),
    path('search/', search, name='search'),
    path('category/<pk>/', category_view, name='category'),
    path("add-comment/<pk>/", add_comment, name="add-comment"),
    path('reply-comment/<pk>/', CommentReplyView.as_view(), name='reply-comment')

]
