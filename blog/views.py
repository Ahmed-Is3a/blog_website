from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.forms import EmailPostForm
from blog.models import Post
from django.core.mail import send_mail

# Create your views here.

class PostListView(ListView):
    # model = Post  # get all posts
    queryset = Post.published.all()  # get published posts 
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


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

def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id, status=Post.Status.PUBLISHED)
    send = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you to read {post.title}"
            )
            message = (
                f"read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comment']}"
            )

            send_mail(subject=subject,message=message,from_email=None, recipient_list=[cd['to']] )
            send = True
    else:
        form = EmailPostForm()

    return render(
        request,
        'post/share.html',
        {
            'post': post,
            'form': form,
            'send': send
        }
    )