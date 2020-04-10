from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from .models import BlogPost
from .models import Category
from django.db.models import Q

class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5 # that is all it takes to add pagination in a Class Based View

    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data(**kwargs)
        context['categories'] =  Category.objects.all()
        context['blog_featured'] = BlogPost.objects.filter(featured=True)
        return context
    
class BlogPostDetailView(DetailView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/detail.html'
    context_object_name = 'blog_post'

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['categories'] =  Category.objects.all()
        context['blog_recent'] = BlogPost.objects.order_by('pub_date')[0:5]
        return context



# def forestry(request):
#     return render(request, 'forestry.html')




def search(request):
    query_set = BlogPost.objects.filter(published=True)
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        queryset = query_set.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query)
        ).distinct()
    
    context = {
        'queryset': queryset,
        'query':query,
        'categories': categories
    }
    return render(request, 'blog/search.html', context)