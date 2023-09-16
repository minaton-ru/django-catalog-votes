from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.forms import modelformset_factory
from .models import Post, Category, Topic
from .forms import NewPostForm, NotApprovedListForm


class LastPostsView(ListView):
    context_object_name = "ten_last_posts"
    template_name = "catalog/index.html"
    queryset = Post.objects.select_related('topic', 'author', 'author__user').prefetch_related('upvotes', 'downvotes').filter(approved=True).order_by("-published")[:10]  # noqa: E501


NotApprovedListFormSet = modelformset_factory(Post,
                                              form=NotApprovedListForm,
                                              edit_only=True,
                                              extra=0)


class NotApprovedListView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy("moderate")
    template_name = "catalog/moderate_list.html"

    def get(self, request):
        queryset = Post.objects.select_related('topic', 'author', 'author__user').prefetch_related('upvotes', 'downvotes').filter(approved=False, rejected=False).order_by("-published")  # noqa: E501
        formset = NotApprovedListFormSet(queryset=queryset)
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        formset = NotApprovedListFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'formset': formset})


class NotApprovedPostView(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy("moderate")
    template_name = "catalog/moderate_post.html"
    model = Post
    fields = ["text", "fromplace", "image",
              "topic", "approved", "rejected"]


def new_post(request):
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        # Если пользователь не авторизован, то автор поста не указывается.
        # Если авторизован - то в автора поста указываем профиль пользователя.
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
    posts = Post.objects.select_related('topic', 'author', 'author__user').prefetch_related('upvotes', 'downvotes').filter(topic__category=category_id)  # noqa: E501
    context = {'posts': posts, 'category': category}
    return render(request, "catalog/category.html", context)


def posts_list_topic(request, category_slug, topic_slug):
    category = get_object_or_404(Category, slug=category_slug)
    topic = get_object_or_404(Topic, slug=topic_slug)
    topic_id = topic.id
    posts = Post.objects.select_related('topic', 'author', 'author__user').prefetch_related('upvotes', 'downvotes').filter(topic=topic_id)  # noqa: E501
    context = {'posts': posts, 'category': category, 'topic': topic}
    return render(request, "catalog/topic.html", context)
