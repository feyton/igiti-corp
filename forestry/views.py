from django.shortcuts import redirect, render, get_object_or_404
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
        context['blog_recent'] = BlogPost.objects.filter(published=True).order_by('-pub_date')[0:5]
        return context




def category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    qs = BlogPost.objects.filter(category = category)
    if qs.exists():
        categories = Category.objects.all()
        context = {
            'blog_posts': qs,
            'categories': categories
        }
        return render(request, 'blog/category.html', context)

    else:
        messages.info(request, 'This category does not have posts yet')
        return redirect('home')




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