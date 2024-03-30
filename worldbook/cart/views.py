from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from cart.cart import Cart
from catalog.models import Book
from .forms import CartAddBookForm


class CartDetailView(TemplateView):
    template_name = 'cart/detail.html'
    extra_context = {
        'title': 'Корзина',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context


class CartAddView(View):
    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        form = CartAddBookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(book=book, quantity=cd['quantity'], override_quantity=cd['override'])

        return redirect('cart:cart')


class CartRemoveView(View):
    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.remove(book)
        return redirect('cart:cart')
