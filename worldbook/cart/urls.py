from django.urls import path
from .views import CartDetailView, CartAddView, CartRemoveView


app_name = 'cart'
urlpatterns = [
    path('', CartDetailView.as_view(), name='cart'),
    path('add/<int:book_id>/', CartAddView.as_view(), name='add'),
    path('remove/<int:book_id>/', CartRemoveView.as_view(), name='remove'),
]
