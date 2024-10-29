from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Profile, UserActivity
from .forms import ProfileForm
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from io import TextIOWrapper
import json
import csv

# Create your views here.
def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def member_list(request):
    """Menampilkan daftar anggota."""
    users = User.objects.all()  # Ambil semua pengguna
    return render(request, 'users/member_list.html', {'users': users})

def register_view(request):
    """Halaman pendaftaran pengguna baru."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Tangkap data dari QR code jika ada
        qr_data = request.POST.get('qr_data', '')
        if qr_data:
            # Asumsikan data QR berisi JSON dengan key username, email, dll.
            try:
                qr_data = json.loads(qr_data)
                username = qr_data.get('username', username)
                email = qr_data.get('email', email)
            except json.JSONDecodeError:
                messages.error(request, 'QR Code tidak valid.')
                return redirect('register')

        # Validasi: Pastikan username dan email tidak duplikat
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah terdaftar. Silakan pilih yang lain.')
            return render(request, 'users/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah terdaftar. Silakan gunakan yang lain.')
            return render(request, 'users/register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        # Membuat profil pengguna baru
        Profile.objects.create(user=user)  # Pastikan profil dibuat
        messages.success(request, 'Akun berhasil dibuat! Silakan login.')
        return redirect('login')

    return render(request, 'users/register.html')


def login_view(request):
    """Halaman login pengguna."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Selamat datang, ' + username + '!')
            return redirect('index')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'users/login.html')

def logout_view(request):
    """Halaman logout pengguna."""
    logout(request)
    messages.success(request, 'Anda telah logout.')
    return redirect('index')

@login_required
def profile_view(request):
    """Halaman informasi pengguna."""
    # Mencatat aktivitas untuk semua pengguna
    UserActivity.objects.create(user=request.user, activity_type='view_profile', timestamp=timezone.now())
    
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'form': form})

def add_member(request):
    """Menambahkan anggota secara manual, melalui CSV."""
    
    if request.method == 'POST':
        if 'manual_add' in request.POST:
            # Penambahan anggota secara manual
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user = User.objects.create_user(username=username, password=password, email=email)
            Profile.objects.create(user=user)
            messages.success(request, f'Anggota {username} berhasil ditambahkan!')
            return redirect('member_list')

        elif 'upload_csv' in request.FILES:
            # Penambahan anggota melalui upload CSV
            csv_file = request.FILES['upload_csv']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File harus berformat CSV.')
                return redirect('add_member')

            data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.reader(data)
            next(reader)  # Skip header
            for row in reader:
                username, email, password = row
                user = User.objects.create_user(username=username, password=password, email=email)
                Profile.objects.create(user=user)

            messages.success(request, 'Anggota dari CSV berhasil ditambahkan!')
            return redirect('member_list')
        
    return render(request, 'users/add_member.html')

def download_csv_template(request):
    """Mengunduh template CSV untuk daftar anggota."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="template_anggota.csv"'

    writer = csv.writer(response)
    writer.writerow(['username', 'email', 'password'])  # Kolom template
    writer.writerow(['user1', 'user1@example.com', 'password123'])  # Contoh baris

    return response

# Ekspor CSV Daftar Anggota
def export_members_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daftar_anggota.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nama Pengguna', 'Email', 'Nomor Telepon', 'Alamat'])

    # Ambil data anggota
    members = Profile.objects.all()
    for member in members:
        writer.writerow([member.id, member.user.username, member.user.email, member.phone_number, member.address])

    return response


@login_required
def get_user_activity(request):
    # Jika admin, ambil semua aktivitas
    if request.user.is_staff:
        activities = UserActivity.objects.all().order_by('timestamp')
    else:
        # Jika pengguna biasa, ambil aktivitas pengguna tersebut
        activities = UserActivity.objects.filter(user=request.user).order_by('timestamp')

    # Format data untuk grafik
    data = {
        'labels': [],
        'data': [],
        'user_types': []
    }

    for activity in activities:
        data['labels'].append(activity.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        data['data'].append(activity.activity_type)

        # Menentukan tipe pengguna
        if activity.user.is_staff:
            data['user_types'].append('admin')
        else:
            data['user_types'].append(activity.user.username)  # Menyimpan nama pengguna

    return JsonResponse(data)
