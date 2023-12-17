from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.forms import modelformset_factory
from django.views.generic.dates import YearArchiveView
from django.db.models import Count

from .models import Post, Category, Topic
from .forms import NewPostForm, NotApprovedListForm


class LastPostsView(ListView):
    """
    Index view, returns ten last posts, ordered by publishing date.
    """
    context_object_name = "ten_last_posts"
    template_name = "catalog/index.html"
    queryset = (
        Post.objects.select_related("topic", "author", "author__user")
        .prefetch_related("upvotes", "downvotes")
        .filter(approved=True)
        .order_by("-published")[:10]
    )


class BestYearView(YearArchiveView):
    """
    Yearly archive with all posts in given year ordered by most voted.
    """
    date_field = "published"
    context_object_name = "best_year_posts"
    template_name = "catalog/best_year.html"
    make_object_list = True

    def get_queryset(self):
        """Returns queryset with posts ordered by the likes and unlikes sum."""
        return (
            Post.objects.select_related("topic", "author", "author__user")
            .prefetch_related("upvotes", "downvotes")
            .filter(approved=True)
            .annotate(votes_result=(Count("upvotes") - Count("downvotes")))
            .order_by("-votes_result")
        )


NotApprovedListFormSet = modelformset_factory(Post,
                                              form=NotApprovedListForm,
                                              edit_only=True,
                                              extra=0)


class NotApprovedListView(PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_post"
    success_url = reverse_lazy("moderate")
    template_name = "catalog/moderate_list.html"

    def get(self, request):
        queryset = (
            Post.objects.select_related('topic', 'author', 'author__user')
            .prefetch_related('upvotes', 'downvotes')
            .filter(approved=False, rejected=False)
            .order_by("-published")
        )
        formset = NotApprovedListFormSet(queryset=queryset)
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        formset = NotApprovedListFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(self.success_url)
        else:
            return render(request, self.template_name, {'formset': formset})


class NotApprovedPostView(PermissionRequiredMixin, UpdateView):
    permission_required = "catalog.change_post"
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


class CategoryView(ListView):
    """
    All posts in category. Gets the category tag from URL.
    """
    context_object_name = "posts"
    template_name = "catalog/category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        category_id = self.category.id
        queryset = (
            Post.objects.select_related('topic', 'author', 'author__user')
            .prefetch_related('upvotes', 'downvotes')
            .filter(topic__category=category_id)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class TopicView(ListView):
    """
    All posts in topic. Gets topic slug and category slug from URL.
    """
    context_object_name = "posts"
    template_name = "catalog/topic.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        self.topic = get_object_or_404(Topic, slug=self.kwargs["topic_slug"])
        topic_id = self.topic.id
        queryset = (
            Post.objects.select_related('topic', 'author', 'author__user')
            .prefetch_related('upvotes', 'downvotes')
            .filter(topic=topic_id)
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        context["topic"] = self.topic
        return context
