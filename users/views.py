from django.shortcuts import render, get_object_or_404
from .models import Profile
from catalog.models import Post


def user_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    user_posts = Post.objects.filter(author=profile)
    context = {'profile': profile, 'user_posts': user_posts}
    return render(request, "users/profile.html", context)
