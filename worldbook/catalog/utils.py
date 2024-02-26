import django_filters
from django.db.models import Q

from .models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['category', 'genre', 'tags', 'authors', 'year']


def search_book(query):
    # Фильтрация по полям модели Book и связанным моделям
    results = Book.objects.filter(
        Q(name__icontains=query) |
        Q(year__icontains=query) |
        Q(authors__first_name__icontains=query) |   # и так далее для authors и tags
        Q(authors__last_name__icontains=query) |
        Q(publisher__icontains=query)         # Для обычного CharField просто publisher
    ).distinct()  # .distinct() используется для избежания дубликатов в результате

    return results
