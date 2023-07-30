from django.forms import ModelForm, FileInput
from .models import Post


class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "fromplace", "image", "topic"]
        labels = {
            'text': 'Надпись',
            'fromplace': 'Откуда (источник)',
            'image': 'Картинка',
            'topic': 'Выберите тему',
        }
        widgets = {
            'image': FileInput(),
        }
        help_texts = {
            'image': 'Или надпись в виде картинки'
        }
