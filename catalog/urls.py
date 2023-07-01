from django.urls import path
from .views import LastPosts

urlpatterns = [
    path("", LastPosts.as_view()),
]
