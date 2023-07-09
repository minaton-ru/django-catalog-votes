from django.urls import path
from . import views 

urlpatterns = [
    path("", views.LastPosts.as_view()),
    path("submit/", views.new_post, name="new_post"),
    path('upvote/<int:post_id>', views.post_upvoting, name='post_upvoting'),
    path('downvote/<int:post_id>', views.post_downvoting, name='post_downvoting'),
]
