from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from catalog.models import Post
from .forms import UserUpdateForm, ProfileUpdateForm


def user_profile(request, pk):
    """
    Отображает публичный профиль пользователя и его присланные работы.
    """
    profile = get_object_or_404(Profile, pk=pk)
    # Если у пользователя есть права на изменение постов
    moderator = profile.user.has_perm('catalog.change_post')
    user_posts = Post.objects.filter(author=profile)
    context = {"profile": profile, "user_posts": user_posts,
               "moderator": moderator}
    return render(request, "users/profile.html", context)


@login_required
def user_account(request):
    user = request.user
    profile = user.profile
    moderator = user.has_perm("catalog.change_post")
    context = {"user": user, "profile": profile, "moderator": moderator}
    return render(request, "users/account.html", context)


class ProfileUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = "users/profile_update.html"
    success_message = "Your account has been updated."

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["user_form"] = UserUpdateForm(self.request.POST,
                                                  instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('user_account')
