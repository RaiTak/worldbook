from django.urls import path
from .views import OrderCreateView, OrderCreatedView


app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create'),
    path('created/', OrderCreatedView.as_view(), name='created'),
]
