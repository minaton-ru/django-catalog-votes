from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.user_profile, name='user_profile'),
]
