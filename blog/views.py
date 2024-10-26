from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()

    paginator = Paginator(posts, 3)
    page_num = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        # posts = paginator.page(paginator.num_pages) # get the last page
        posts = paginator.page(1)  # get the first page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # get the last page
        # posts = paginator.page(1)  # get the first page

    return render(
        request,
        'post/list.html',
        {'posts': posts}
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post, publish__year=year, publish__month=month,
        publish__day=day)

    return render(
        request,
        'post/detail.html',
        {'post': post}
    )
