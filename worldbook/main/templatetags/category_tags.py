from django import template
from catalog.models import Category

register = template.Library()


@register.simple_tag()
def get_categories():
    res = Category.objects.all()
    return res


@register.inclusion_tag('catalog/list_category.html')
def show_categories(cat_selected):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}