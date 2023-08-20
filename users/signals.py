from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from users.models import Profile


@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    '''
    Обрабатывает сигнал о регистрации пользователя от allauth.
    Создает профиль для зарегистрированного пользователя.
    '''
    Profile.objects.create(user=user)
