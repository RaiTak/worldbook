from django.urls import path
from catalog import views


app_name = 'catalog'
urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('book/<slug:book_slug>/', views.book, name='book'),
    path('<str:type>/<slug:slug>/', views.BookList.as_view(), name='book_list'),
]
