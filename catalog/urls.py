from django.urls import path
from . import views

urlpatterns = [
    path("", views.LastPostsView.as_view(), name="index"),
    path("best/<int:year>/", views.BestYearView.as_view(), name="best_year"),
    path("moderate/", views.NotApprovedListView.as_view(), name="moderate"),
    path("moderate/<int:pk>/",
         views.NotApprovedPostView.as_view(), name="moderate_post"),
    path("submit/", views.new_post, name="new_post"),
    path('upvote/<int:post_id>',
         views.post_upvoting, name='post_upvoting'),
    path('downvote/<int:post_id>',
         views.post_downvoting, name='post_downvoting'),
    path('<slug:category_slug>/',
         views.posts_list_category, name="posts_list_category"),
    path('<slug:category_slug>/<slug:topic_slug>/',
         views.posts_list_topic, name="posts_list_topic"),
]
