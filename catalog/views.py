from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from .models import Post, Category, Topic
from .forms import NewPostForm


class LastPosts(ListView):
    context_object_name = "ten_last_posts"
    queryset = Post.objects.filter(approved=True).order_by("-published")[:10]
    template_name = "catalog/index.html"


def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if request.user.is_anonymous:
            author = None
        else:
            author = request.user.profile
        if form.is_valid():
            post = form.save()
            post.author = author
            post.save()
            return redirect("/")
    else:
        form = NewPostForm()
    return render(request, "catalog/submit.html", {"form": form})


@login_required(redirect_field_name=None)
def post_upvoting(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if post.upvotes.filter(id=request.user.id).exists():
            post.upvotes.remove(request.user)
        else:
            post.upvotes.add(request.user)
            if post.downvotes.filter(id=request.user.id).exists():
                post.downvotes.remove(request.user)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(redirect_field_name=None)
def post_downvoting(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        if post.downvotes.filter(id=request.user.id).exists():
            post.downvotes.remove(request.user)
        else:
            post.downvotes.add(request.user)
            if post.upvotes.filter(id=request.user.id).exists():
                post.upvotes.remove(request.user)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def posts_list_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    category_id = category.id
    posts = Post.objects.filter(topic__category=category_id)
    context = {'posts': posts, 'category': category}
    return render(request, "catalog/category.html", context)


def posts_list_topic(request, category_slug, topic_slug):
    category = get_object_or_404(Category, slug=category_slug)
    topic = get_object_or_404(Topic, slug=topic_slug)
    topic_id = topic.id
    posts = Post.objects.filter(topic=topic_id)
    context = {'posts': posts, 'category': category, 'topic': topic}
    return render(request, "catalog/topic.html", context)
