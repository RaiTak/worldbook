from django.urls import path
from .views import payment_completed, payment_canceled, payment_process
from .application import webhooks

app_name = 'payment'
urlpatterns = [
    path('process/', payment_process, name='process'),
    path('completed/', payment_completed, name='completed'),
    path('canceled/', payment_canceled, name='canceled'),
    path('webhooks/', webhooks.stripe_webhook, name='stripe-webhook'),
]
