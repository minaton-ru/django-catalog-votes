from django.contrib import admin
from .models import Category, Topic, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]


class TopicAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "category"]


class PostAdmin(admin.ModelAdmin):
    list_display = ["__str__", "topic", "approved", "published"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
