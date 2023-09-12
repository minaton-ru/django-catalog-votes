from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileInput
from .models import Post, Profile, Topic


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "fromplace", "image", "topic"]
        labels = {
            "text": "Надпись",
            "fromplace": "Откуда (источник)",
            "image": "Картинка",
            "topic": "Выберите тему",
        }
        widgets = {
            "image": FileInput(),
        }
        help_texts = {
            "image": "Или надпись в виде картинки"
        }


class NotApprovedListForm(ModelForm):
    author = forms.ModelChoiceField(queryset=Profile.objects.all(),
                                    disabled=True,
                                    required=False)
    text = forms.CharField(disabled=True)
    fromplace = forms.CharField(disabled=True)
    image = forms.ImageField(disabled=True, required=False)
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(),
                                   disabled=True, required=False)

    def clean(self):
        cleaned_data = super().clean()
        # Approved and Rejected at the same time are not allowed
        if cleaned_data.get("approved") and cleaned_data.get("rejected"):
            raise ValidationError(
                "Нельзя одновременно ставить approved и rejected"
                )

    class Meta:
        model = Post
        fields = ["text", "fromplace", "image",
                  "topic", "author", "approved", "rejected"]
        help_texts = {
            "approved": "Можно публиковать без редактирования",
            "rejected": "Нельзя публиковать ни в каком виде"
        }
