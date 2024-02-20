import django_filters
from .models import Product


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['year', 'category']