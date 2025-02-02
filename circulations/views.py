from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, ActivityLog
from books.models import Book
from users.models import Profile
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
import csv

# Create your views here.
@login_required
def borrow_book(request):
    """Meminjam buku."""
    books = Book.objects.filter(stock__gt=0)  # Hanya ambil buku dengan stok lebih dari 0
    
    # Pastikan profil pengguna ada
    if not hasattr(request.user, 'profile'):
        messages.error(request, 'Profil pengguna tidak ditemukan. Silakan hubungi admin.')
        return redirect('index')  # Ganti dengan halaman yang sesuai

    if request.method == 'POST':
        book_id = request.POST['book_id']
        book = get_object_or_404(Book, id=book_id)

        if book.stock > 0:
            transaction = Transaction(book=book, user=request.user.profile)
            transaction.save()
            book.stock -= 1
            book.save()
            messages.success(request, 'Buku berhasil dipinjam!')
            return redirect('book_list')
        else:
            messages.error(request, 'Stok buku tidak tersedia.')

    return render(request, 'transactions/borrow_book.html', {'books': books})


@login_required
def return_book(request):
    """Mengembalikan buku."""
    if request.method == 'POST':
        transaction_id = request.POST['transaction_id']
        transaction = get_object_or_404(Transaction, id=transaction_id)

        transaction.book.stock += 1
        transaction.book.save()
        transaction.delete()
        messages.success(request, 'Buku berhasil dikembalikan!')
        return redirect('book_list')

    transactions = Transaction.objects.filter(user=request.user.profile)
    return render(request, 'transactions/return_book.html', {'transactions': transactions})

@login_required
def loan_list(request):
    """Menampilkan daftar pinjaman berdasarkan peran pengguna."""
    if request.user.is_superuser:
        transactions = Transaction.objects.all()  # Semua transaksi untuk admin
    else:
        transactions = Transaction.objects.filter(user=request.user.profile)  # Transaksi user biasa

    # Pagination logic: display 10 transactions per page
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')  # Get current page number from query string
    page_obj = paginator.get_page(page_number)  # Get the page object based on the current page number

    
    # Logika untuk mengembalikan buku
    if request.method == 'POST':
        transaction_ids = request.POST.getlist('transaction_ids')
        for transaction_id in transaction_ids:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            if not transaction.return_date:  # Pastikan buku belum dikembalikan
                transaction.book.stock += 1
                transaction.book.save()
                transaction.return_date = timezone.now()  # Tanggal pengembalian
                transaction.save()
                messages.success(request, 'Buku berhasil dikembalikan!')

        return redirect('loan_list')

    return render(request, 'transactions/loan_list.html', {'transactions': page_obj})

@login_required
def return_list(request):
    """Menampilkan daftar buku yang sudah dikembalikan."""
    if request.user.is_superuser:
        transactions = Transaction.objects.filter(return_date__isnull=False)  # Semua pengembalian
    else:
        transactions = Transaction.objects.filter(user=request.user.profile, return_date__isnull=False)  # Pengembalian user biasa

    # Pagination logic: display 10 transactions per page
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')  # Get current page number from query string
    page_obj = paginator.get_page(page_number)  # Get the page object based on the current page number

    return render(request, 'transactions/return_list.html', {'transactions': page_obj})

@login_required
def edit_loan(request, loan_id):
    """Mengedit informasi pinjaman buku."""
    loan = get_object_or_404(Transaction, id=loan_id)
    
    if request.method == 'POST':
        loan.book = get_object_or_404(Book, id=request.POST['book_id'])
        loan.borrowed_date = request.POST['borrowed_date']
        loan.return_date = request.POST['return_date']
        loan.save()
        messages.success(request, 'Pinjaman berhasil diperbarui!')
        return redirect('loan_list')

    return render(request, 'circulations/edit_loan.html', {'loan': loan})

@login_required
def delete_loan(request, loan_id):
    """Menghapus data pinjaman."""
    loan = get_object_or_404(Transaction, id=loan_id)
    loan.delete()
    messages.success(request, 'Pinjaman berhasil dihapus!')
    return redirect('loan_list')

# Ekspor CSV Daftar Peminjaman
def export_loans_csv(request):
    # Buat HTTP response dengan tipe konten CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daftar_peminjaman.csv"'

    # Tentukan header kolom CSV
    writer = csv.writer(response)
    writer.writerow(['ID', 'Buku', 'Pengguna', 'Tanggal Pinjam'])

    # Ambil data peminjaman
    loans = Transaction.objects.all()
    for loan in loans:
        writer.writerow([loan.id, loan.book.title, loan.user.user.username, loan.borrowed_date])

    return response

def export_returns_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daftar_pengembalian.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Buku', 'Pengguna', 'Tanggal Kembali'])

    # Ambil data pengembalian, sesuaikan dengan model pengembalian
    returns = Transaction.objects.filter(return_date__isnull=False)
    for return_ in returns:
        writer.writerow([return_.id, return_.book.title, return_.user.user.username, return_.return_date])

    return response


@login_required
def add_loan(request):
    """Menambahkan pinjaman baru secara manual untuk admin."""
    if not request.user.is_superuser:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect("loan_list")

    profiles = Profile.objects.all()  # Semua pengguna yang dapat dipilih sebagai peminjam
    books = Book.objects.filter(stock__gt=0)  # Hanya buku dengan stok tersedia

    if request.method == "POST":
        user_id = request.POST["user_id"]
        book_id = request.POST["book_id"]
        borrowed_date = request.POST["borrowed_date"]

        user = get_object_or_404(Profile, id=user_id)
        book = get_object_or_404(Book, id=book_id)

        if book.stock > 0:
            transaction = Transaction(user=user, book=book, borrowed_date=borrowed_date)
            transaction.save()
            book.stock -= 1
            book.save()
            messages.success(request, "Pinjaman baru berhasil ditambahkan.")
            return redirect("loan_list")
        else:
            messages.error(request, "Stok buku tidak tersedia.")

    return render(request, "transactions/add_loan.html", {"profiles": profiles, "books": books})


@login_required
def add_return(request):
    """Menambahkan pengembalian buku secara manual untuk admin."""
    if not request.user.is_superuser:
        messages.error(request, "Anda tidak memiliki izin untuk mengakses halaman ini.")
        return redirect("loan_list")

    # Hanya menampilkan transaksi pinjaman yang belum dikembalikan
    transactions = Transaction.objects.filter(return_date__isnull=True)

    if request.method == "POST":
        transaction_id = request.POST["transaction_id"]
        return_date = request.POST["return_date"]

        transaction = get_object_or_404(Transaction, id=transaction_id)

        # Memperbarui stok buku dan tanggal pengembalian
        transaction.return_date = return_date
        transaction.book.stock += 1
        transaction.book.save()
        transaction.save()
        messages.success(request, "Pengembalian berhasil ditambahkan.")
        return redirect("loan_list")

    return render(request, "transactions/add_return.html", {"transactions": transactions})


def reward_system(request):
    """Menampilkan reward berdasarkan aktivitas siswa."""
    if request.method == 'POST':
        # Logika untuk memberikan reward
        user_activity_count = ActivityLog.objects.filter(user=request.user.profile).count()
        # Misalnya, berikan reward jika aktivitas lebih dari 10
        if user_activity_count > 10:
            # Logika untuk memberikan reward
            messages.success(request, 'Selamat! Anda telah mendapatkan reward!')
        else:
            messages.info(request, 'Teruslah beraktivitas untuk mendapatkan reward!')

    return render(request, 'transactions/reward_system.html', {
        'activity_count': ActivityLog.objects.filter(user=request.user.profile).count(),
    })
    
    
@staff_member_required
def activity_chart(request):
    # hitung jumlah aktivitas per siswa
    activity_data = ActivityLog.objects.values('user__user__username').annotate(activity_count=Count('id'))
    
    # persiapkan data untuk grafik
    labels = [data['user__user__username'] for data in activity_data]
    counts = [data['activity_count'] for data in activity_data]
    
    return render(request, 'transactions/activity_chart.html', {
        'labels': labels,
        'counts': counts,
    })