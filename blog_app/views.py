from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

from .forms import LoginForm, RegisterForm, PostForm, CommentForm
from .models import Post
from django.contrib.auth import  login as dlogin, logout as dlogout

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class PostList(generic.ListView):
    def setup(self, request, *args, **kwargs):
        request.session['username'] = 'Ayush'
        super(PostList, self).setup(request)

    queryset = Post.objects.filter(status=Post.Status.PUBLISH).order_by('-created_on')
    template_name = 'index.html'
    #
    # def get_query(self):
    #     return self.request.user


# @cache_page(CACHE_TTL)
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if request.user.is_anonymous:
            messages.warning(request, 'Please Login to make a Comment.')
            return HttpResponseRedirect(reverse('post_login'))
        else:
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.comment_maker = request.user
                new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

#
# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#     queryset = Post.objects.all()


@login_required(login_url='/blog/login/')
def post_maker(request):
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            messages.success(request, 'Post Made. Wait for the Admin To Verify and Publish it.')
        return HttpResponseRedirect(reverse('home'))
    else:
        form = PostForm()
        return render(request, 'post_maker.html', context={'form': form})


class AuthorPosts(generic.ListView):
    model = Post
    template_name = 'author_posts.html'

    def get_queryset(self):
        queryset = super(AuthorPosts, self).get_queryset()
        return queryset.filter(author=self.request.user).order_by('-created_on')
#
#     queryset = Post.objects.filter(author=)
# #
# def author_posts(request):
#     posts = [p for p in Post.objects.filter(author=request.user)]
#     return render(request, 'author_posts.html',
#                   context={'posts': posts}
#                   )


def login(request):
    if request.POST:
        visitor = LoginForm(request.POST)
        if visitor.is_valid():
            user = visitor.save()
            if user is not None:
                dlogin(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Wrong")
    return render(request, 'login.html')


def logout(request):
    dlogout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):
    if request.POST:
        print(request.POST)
        v = RegisterForm(request.POST)
        if v.is_valid():
            v.create()
            return HttpResponseRedirect(reverse('post_login'))
    print("IN REGISTER")
    return render(request, 'register.html')

