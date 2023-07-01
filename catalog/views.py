from django.shortcuts import render
from django.views.generic import ListView
from catalog.models import Post

class LastPosts(ListView):
    context_object_name = "ten_last_posts"
    queryset = Post.objects.filter(approved=True).order_by("-published")[:10]
    template_name = "catalog/index.html"