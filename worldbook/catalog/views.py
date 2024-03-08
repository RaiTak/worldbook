from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from catalog.models import Category, Book, Genre, Tag, Author
from .utils import BookFilter, search_book
from django.http import Http404


MODEL_MAP = {
        'category': Category,
        'genre': Genre,
        'tag': Tag,
        'author': Author,
    }


class CatalogView(ListView):
    model = Book
    template_name = 'catalog/catalog.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = BookFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        type = self.kwargs.get('type').lower()
        slug = self.kwargs.get('slug')

        model = MODEL_MAP.get(type)
        if not model:
            raise Http404("Type not found")

        obj = get_object_or_404(model.objects.prefetch_related(
            Prefetch('books', queryset=Book.objects.all())
        ), slug=slug)

        return obj.books.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.kwargs.get('type').lower()
        slug = self.kwargs.get('slug')
        model = MODEL_MAP.get(type)
        obj = get_object_or_404(model, slug=slug)
        context['content'] = obj
        context['title'] = obj
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/product.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class BookSearchView(ListView):
    model = Book
    template_name = 'catalog/search_book.html'
    context_object_name = 'content'
    paginate_by = 1

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            results = search_book(query)
        else:
            results = Book.objects.none()
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск'
        return context