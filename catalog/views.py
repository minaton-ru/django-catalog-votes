from django.shortcuts import render, redirect
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
