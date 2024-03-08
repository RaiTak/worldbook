import django_filters
from django.db.models import Q

from .models import Book


class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = ['category', 'genre', 'tags', 'authors', 'year']


def search_book(query):
    results = Book.objects.filter(
        Q(name__icontains=query) |
        Q(year__icontains=query) |
        Q(authors__first_name__icontains=query) |
        Q(authors__last_name__icontains=query) |
        Q(publisher__icontains=query)
    ).distinct()

    return results
