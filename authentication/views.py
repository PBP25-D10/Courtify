# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile

# === Views untuk menampilkan halaman HTML ===

def login_page_view(request):
    """Menampilkan halaman dengan form login."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/login.html')

def register_page_view(request):
    """Menampilkan halaman dengan form register."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/register.html')

def dashboard_view(request):
    """Halaman yang hanya bisa diakses setelah login."""
    if not request.user.is_authenticated:
        return redirect('authentication:login_page')
    return render(request, 'authentication/dashboard.html')


# === Views API untuk ditangani oleh AJAX ===

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role') # <-- 2. Ambil data 'role'

        # Validasi
        if not all([username, password, email, role]):
            return JsonResponse({'status': 'error', 'message': 'Semua field harus diisi.'}, status=400)
        
        # Validasi tambahan untuk role
        if role not in ['user', 'penyedia']:
            return JsonResponse({'status': 'error', 'message': 'Peran tidak valid.'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username sudah digunakan.'}, status=400)

        # Buat user baru
        user = User.objects.create_user(username=username, password=password, email=email)
        
        # <-- 3. Buat UserProfile yang terhubung dengan role yang dipilih
        UserProfile.objects.create(user=user, role=role)

        return JsonResponse({'status': 'success', 'message': 'Registrasi berhasil! Silakan login.'})
    
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Buat response JSON
            response = JsonResponse({
                'status': 'success',
                'message': 'Login berhasil!',
                'redirect_url': '/'  # <-- Arahkan ke root URL!
            })
            
            # **Membuat Cookie Sederhana**
            # Simpan nama depan pengguna di cookie selama 1 hari (86400 detik)
            response.set_cookie('user_firstname', user.first_name or user.username, max_age=86400) 
            
            return response
        else:
            return JsonResponse({'status': 'error', 'message': 'Username atau password salah.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        logout(request)
        response = JsonResponse({'status': 'success', 'message': 'Logout berhasil.', 'redirect_url': reverse('authentication:login_page')})

        # Hapus cookie yang kita buat
        response.delete_cookie('user_firstname')

        return response

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)

def logout_page_view(request):
    logout(request)
    response = redirect('authentication:login_page')
    response.delete_cookie('user_firstname')
    return response

