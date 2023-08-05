from django import template
from catalog.models import Category

register = template.Library()


@register.inclusion_tag("catalog/tags/category_list.html")
def show_category_list():
    all_categories_list = Category.objects.all()
    return {"all_categories_list": all_categories_list}
