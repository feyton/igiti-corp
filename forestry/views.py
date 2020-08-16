from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from store.models import OrderItem

from .models import BlogPost, Category


class BlogPostListView(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5  # that is all it takes to add pagination in a Class Based View

    def get_context_data(self, **kwargs):
        context = super(BlogPostListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['blog_featured'] = BlogPost.objects.filter(featured=True)
        return context


class BlogPostDetailView(HitCountDetailView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    template_name = 'blog/detail.html'
    context_object_name = 'blog_post'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['blog_recent'] = BlogPost.objects.filter(
            published=True).order_by('-pub_date')[0:5]
        context.update({
            'popular_posts': BlogPost.objects.filter(published=True).order_by('-hit_count_generic__hits')[:5],
        })
        return context


def category_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    qs = BlogPost.objects.filter(published=True, category=category)
    # if qs.exists():
    categories = Category.objects.all()
    context = {
        'blog_posts': qs,
        'categories': categories,
        'category': category
    }
    return render(request, 'blog/category.html', context)

    # else:
    #     return HttpResponse('<div class="trending-post"><h5>Sorry, we do not have posts in this category yet</h5</div>')


def search(request):
    query_set = BlogPost.objects.filter(published=True)
    query = request.GET.get('q')
    categories = Category.objects.all()
    if query:
        queryset = query_set.filter(
            Q(title__icontains=query) | Q(text__icontains=query) | Q(category__title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        context = {
            'queryset': queryset,
            'query': query,
            'categories': categories
        }
        return render(request, 'blog/search.html', context)
    else:
        messages.error(request, "Type a valid term")
        return redirect('forestry:list')



