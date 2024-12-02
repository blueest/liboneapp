from django.urls import path
from .views import index, book_list, book_detail, add_book, edit_book, delete_book, search_books, online_books, detail_online_book, download_books_template, import_books_csv

urlpatterns = [
    path('', index, name='index'),
    path('book/', book_list, name='book_list'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),
    path('add/', add_book, name='add_book'),
    path('edit/<int:book_id>/', edit_book, name='edit_book'),
    path('delete/<int:book_id>/', delete_book, name='delete_book'),
    path('search/', search_books, name='search_books'),
    path('online/', online_books, name='online_books'),
    path('online/<int:pk>/', detail_online_book, name='detail_online_book'),
    path('import-csv/', import_books_csv, name='import_books_csv'),
    path('download-template/', download_books_template, name='download_books_template'),
]