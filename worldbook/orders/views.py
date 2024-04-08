from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:created')
    extra_context = {
        'title': 'Заказ',
    }

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order, book=item['book'], price=item['price'], quantity=item['quantity'])

        cart.clear()
        order_created.delay(order.id)
        self.request.session['order_id'] = order.pk
        return redirect(reverse('payment:process'))


class OrderCreatedView(TemplateView):
    template_name = 'orders/created.html'
    extra_context = {
        'title': 'Успешный заказ',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        context['order_id'] = order_id
        return context
