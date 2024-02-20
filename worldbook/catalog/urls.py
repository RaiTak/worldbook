from django.urls import path
from catalog import views


app_name = 'catalog'
urlpatterns = [
    path('', views.catalog, name='catalog_all'),
    path('books/', views.book_list, name='book_list'),
    path('<slug:category_slug>/', views.catalog, name='catalog'),
    path('book/<slug:book_slug>/', views.book, name='book'),
]
