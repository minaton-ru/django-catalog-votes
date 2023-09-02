from django.forms import ModelForm, FileInput
from django.contrib.auth.models import User
from .models import Profile


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        labels = {
            "avatar": "Аватар",
        }
        widgets = {
            "avatar": FileInput(),
        }
        help_texts = {
            "avatar": "Картинка вашего аватара"
        }
