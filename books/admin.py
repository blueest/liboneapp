from django.contrib import admin
from .models import Book, OnlineBook

# Register your models here.
admin.site.register(Book)
admin.site.register(OnlineBook)