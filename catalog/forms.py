from django.forms import ModelForm, FileInput
from .models import Post

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["text", "fromplace", "image", "category", "topic"]
        labels = {
            'text': 'Надпись',
            'fromplace': 'Откуда (источник)',
            'image': 'Картинка',
            'category': 'Выберите общую категорию',
            'topic': 'Выберите тему из категории',
        }
        widgets = {
            'image': FileInput(),
        }
        help_texts = {
            'image': 'Или надпись в виде картинки'
        }
