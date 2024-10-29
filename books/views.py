from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, OnlineBook
from django.contrib import messages
from .forms import SearchForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def book_list(request):
    # Menampilkan daftar semua buku
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, book_id):
    """Menampilkan detail buku tertentu."""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book})

def add_book(request):
    """Menambahkan buku baru ke dalam sistem."""
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        published_date = request.POST['published_date']
        stock = request.POST['stock']
        
        new_book = Book(title=title, author=author, published_date=published_date, stock=stock)
        new_book.save()
        messages.success(request, 'Buku berhasil ditambahkan!')
        return redirect('book_list')
    
    return render(request, 'books/add_book.html')

def edit_book(request, book_id):
    """Mengedit informasi buku."""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author = request.POST['author']
        book.published_date = request.POST['published_date']
        book.stock = request.POST['stock']
        book.save()
        messages.success(request, 'Buku berhasil diperbarui!')
        return redirect('book_list')

    return render(request, 'books/edit_book.html', {'book': book})

def delete_book(request, book_id):
    """Menghapus buku dari sistem."""
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Buku berhasil dihapus!')
    return redirect('book_list')

def search_books(request):
    form = SearchForm()
    results = []

    if request.method == "GET":
        query = request.GET.get('query')
        if query:
            results = Book.objects.filter(title__icontains=query)

    return render(request, 'search_results.html', {'form': form, 'results': results})

def online_books(request):
    books = OnlineBook.objects.filter(availability='online')
    return render(request, 'books/online_books.html', {'books': books})

def detail_online_book(request, pk):
    book = get_object_or_404(OnlineBook, pk=pk)
    return render(request, 'books/detail_online_book.html', {'book': book})