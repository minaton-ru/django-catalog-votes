from django.forms import ModelForm, FileInput
from django.forms import modelformset_factory
from .models import Post


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


class NotApprovedPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "fromplace", "image",
                  "topic", "author", "approved", "rejected"]
        help_texts = {
            "approved": "Можно публиковать без редактирования",
            "rejected": "Нельзя публиковать ни в каком виде"
        }


NotApprovedPostFormSet = modelformset_factory(Post,
                                              form=NotApprovedPostForm,
                                              edit_only=True)
