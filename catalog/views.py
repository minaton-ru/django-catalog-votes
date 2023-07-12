from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from .models import Post
from .forms import NewPostForm

class LastPosts(ListView):
    context_object_name = "ten_last_posts"
    queryset = Post.objects.filter(approved=True).order_by("-published")[:10]
    template_name = "catalog/index.html"

def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = NewPostForm()
    return render(request, "catalog/submit.html", {"form": form})

@login_required()
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

@login_required()
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