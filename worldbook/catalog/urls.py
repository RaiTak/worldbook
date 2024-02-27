from django.urls import path
from catalog import views


app_name = 'catalog'
urlpatterns = [
    path('', views.CatalogView.as_view(), name='catalog'),
    path('search/', views.BookSearchView.as_view(), name='search'),
    path('book/<slug:book_slug>/', views.BookDetailView.as_view(), name='book'),
    path('<str:type>/<slug:slug>/', views.BookListView.as_view(), name='book_list'),
]
