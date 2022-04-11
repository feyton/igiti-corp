from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from modeltranslation.admin import TranslationAdmin

from .models import Author, BlogPost, Category, Comment, CommentReply


def approve_comments(ModelAdmin, request, queryset):
    queryset.update(approved='True')


approve_comments.set_description = 'Approve comments'


def remove_comments(ModelAdmin, request, queryset):
    queryset.delete()


remove_comments.set_description = 'Delete comments'


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'published', 'pub_date')


admin.site.register(BlogPost, BlogPostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'message', 'approved')
    list_filter = ('approved',)
    actions = [approve_comments, remove_comments]
    ordering = ['approved', 'full_name']


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(CommentReply)
