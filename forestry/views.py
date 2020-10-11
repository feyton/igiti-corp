from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from hitcount.views import HitCountDetailView
from store.models import OrderItem

from .forms import CommentForm, CommentReplyForm, UserCommentForm
from .models import BlogPost, Category, Comment, CommentReply


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
        if not self.request.user.is_authenticated:
            context['form'] = CommentForm
        else:
            context['form'] = UserCommentForm
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


def add_comment(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user.is_authenticated:
        form = UserCommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.full_name = request.user.get_full_name()
            comment.email = request.user.email
            comment.post = post
            comment.approved = True
            comment.save()
            messages.success(request, "Thank you for commenting")
            return redirect(post)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, "Thank you for your contribution")
        return redirect(post)
    messages.error(request, "Please fill the form correctly")
    return redirect(post)


def reply_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    return redirect(post)


@method_decorator(login_required, name='dispatch')
class CommentReplyView(View):
    def get(self, *args, **kwargs):
        pk = self.kwargs['pk']
        context = {'pk': pk, 'form': CommentReplyForm}
        return render(self.request, "blog/reply-form.html", context)

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        comment = get_object_or_404(Comment, pk=pk)
        post = comment.post
        form = CommentReplyForm(self.request.POST or None)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = self.request.user
            reply.save()
            return redirect(post)
        return redirect(post)
