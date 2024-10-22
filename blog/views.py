from django.http import Http404
from django.shortcuts import render

from blog.models import Post

# Create your views here.

def post_list(request):
    posts = Post.published.all()

    return render(
        request,
        'blog/post/posts.html',
        {'posts': posts}
    )
