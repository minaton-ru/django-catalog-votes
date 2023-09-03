from django.urls import path
from .views import ProfileUpdateView
from . import views

urlpatterns = [
    path('profile/<int:pk>', views.user_profile, name='user_profile'),
    path('accounts/user/', views.user_account, name='user_account'),
    path('profile/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
]
