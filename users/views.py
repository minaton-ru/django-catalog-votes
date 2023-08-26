from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from catalog.models import Post


def user_profile(request, pk):
    '''
    Отображает публичный профиль пользователя и его присланные работы.
    '''
    profile = get_object_or_404(Profile, pk=pk)
    # Если у пользователя есть права на изменение постов
    moderator = profile.user.has_perm('catalog.change_post')
    user_posts = Post.objects.filter(author=profile)
    context = {'profile': profile, 'user_posts': user_posts,
               'moderator': moderator}
    return render(request, "users/profile.html", context)


@login_required
def user_account(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    moderator = user.has_perm('catalog.change_post')
    context = {'user': user, 'profile': profile, 'moderator': moderator}
    return render(request, "users/account.html", context)
