from django.contrib import admin

from .models import Author, BlogPost, Category, Comment, CommentReply


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'published', 'pub_date')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(CommentReply)
