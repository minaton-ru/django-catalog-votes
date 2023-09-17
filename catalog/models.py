from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from users.models import Profile


class Category(models.Model):
    name = models.CharField('category', max_length=20)
    slug = models.SlugField()

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField('topic', max_length=20)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='topics')

    class Meta:
        ordering = ['id']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL,
                               null=True, blank=True)
    text = models.TextField(max_length=2000)
    fromplace = models.TextField(max_length=50)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/",
                              null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,
                              null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='post_upvotes',
                                     blank=True)
    downvotes = models.ManyToManyField(User, related_name='post_downvotes',
                                       blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published']
        verbose_name = 'Надпись'
        verbose_name_plural = 'Надписи'

    def clean(self):
        # Approved and Rejected at the same time are not allowed
        if self.approved and self.rejected:
            raise ValidationError(
                "Нельзя одновременно ставить approved и rejected",
                code="invalid"
                )

    def get_total_upvotes(self) -> int:
        return self.upvotes.count()

    def get_total_downvotes(self) -> int:
        return self.downvotes.count()

    def get_votes_result(self) -> int:
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("moderate_post", kwargs={"pk": self.pk})
