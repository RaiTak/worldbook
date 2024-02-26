from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Book, Genre, Tag, Author
from .utils import BookFilter
from django.views import View
from django.http import Http404


MODEL_MAP = {
        'category': Category,
        'genre': Genre,
        'tag': Tag,
        'author': Author,
    }


def catalog(request):
    book_filter = BookFilter(request.GET, queryset=Book.objects.all())

    context = {
        'title': 'Каталог',
        'filter': book_filter,
    }

    return render(request, template_name='catalog/catalog.html', context=context)


def book(request, book_slug):
    book = Book.objects.get(slug=book_slug)
    cat_selected = book.category.slug

    context = {
        'title': book.name,
        'book': book,
        'cat_selected': cat_selected,
    }

    return render(request, template_name='catalog/product.html', context=context)


class BookList(View):

    def get(self, request, type, slug):
        model = MODEL_MAP.get(type.lower())
        if not model:
            raise Http404("Type not found")

        obj = get_object_or_404(model, slug=slug)

        context = {
            'title': obj,
            'content': obj,
        }

        return render(request, template_name='catalog/book_list.html', context=context)