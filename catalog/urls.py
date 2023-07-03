from django.urls import path
from . import views 

urlpatterns = [
    path("", views.LastPosts.as_view()),
    path("submit/", views.new_post, name="new_post"),
]
