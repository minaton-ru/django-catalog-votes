from django.db import models
from django.contrib.auth.models import User
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
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, null=True, default="Other")
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'
    
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_DEFAULT, null=True, blank=True, default="Other")
    text = models.TextField(max_length=2000)
    fromplace = models.TextField(max_length=50)
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, null=True, default="Other")
    topic = models.ForeignKey(Topic, on_delete=models.SET_DEFAULT, null=True, default="Other")
    published = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-published']
        verbose_name = 'Надпись'
        verbose_name_plural = 'Надписи'
    
    def number_of_likes(self):
        if self.likes.count() == 0:
            return ''
        else:
            return self.likes.count()

    def __str__(self):
        return self.text
