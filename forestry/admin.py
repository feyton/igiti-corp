from django.contrib import admin
from .models import BlogPost
from .models import Author
from .models import Category




@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'published', 'pub_date')


admin.site.register(Author)
admin.site.register(Category)