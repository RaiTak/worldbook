from django.shortcuts import render
from catalog.models import Category, Product
from .utils import BookFilter


def catalog(request, category_slug=None):
    book_filter = BookFilter(request.GET, queryset=Product.objects.all())
    if category_slug:
        cat = Category.objects.get(slug=category_slug)
        books = cat.books.all()
    else:
        books = Product.objects.all()

    context = {
        'title': 'Каталог',
        'filter': book_filter,
        'category': category,
        'cat_selected': category_slug,

    }

    return render(request, template_name='catalog/catalog.html', context=context)


def book(reqeust, book_slug):
    book = Product.objects.get(slug=book_slug)
    cat_selected = book.category.slug

    context = {
        'title': 'Книга',
        'book': book,
        'cat_selected': cat_selected,
    }

    return render(reqeust, template_name='catalog/product.html', context=context)


def book_list(request):
    book_filter = BookFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'catalog/book_list.html', {'filter': book_filter})