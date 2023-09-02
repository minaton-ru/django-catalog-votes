from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('аватар', null=True, blank=True,
                               upload_to='uploads/profiles/%Y/%m/',
                               default='uploads/profiles/default.jpg')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"pk": self.pk})
