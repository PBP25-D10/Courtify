# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# ==============================================================================
# PERBAIKAN KRITIKAL DI SINI
# Kita menggunakan 'as' untuk memberikan nama alias pada fungsi login dan logout
# bawaan Django. Ini MENCEGAH BENTROK nama dengan fungsi view Anda sendiri.
# ==============================================================================
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# ==============================================================================

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile

# ==============================================================================
# BAGIAN 1: Views untuk Halaman HTML Biasa (Django Template)
# ==============================================================================

def login_page_view(request):
    """Menampilkan halaman dengan form login HTML."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/login.html')

def register_page_view(request):
    """Menampilkan halaman dengan form register HTML."""
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/register.html')

def dashboard_view(request):
    """Halaman dashboard HTML yang hanya bisa diakses setelah login."""
    if not request.user.is_authenticated:
        return redirect('authentication:login_page')
    return render(request, 'authentication/dashboard.html')

def logout_page_view(request):
    """View untuk menangani logout dari halaman web biasa dan redirect."""
    # Gunakan alias auth_logout
    auth_logout(request)
    # Pastikan nama URL redirect ini benar sesuai urls.py Anda (misal 'authentication:login_page')
    response = redirect('authentication:login_page') 
    response.delete_cookie('user_firstname')
    return response


# ==============================================================================
# BAGIAN 2: Views API Standar (Misal untuk AJAX di Web)
# ==============================================================================

@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            role = data.get('role')

            # Validasi
            if not all([username, password, email, role]):
                return JsonResponse({'status': 'error', 'message': 'Semua field harus diisi.'}, status=400)
            
            # Validasi role
            if role not in ['user', 'penyedia']:
                return JsonResponse({'status': 'error', 'message': 'Peran tidak valid.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username sudah digunakan.'}, status=400)

            # Buat user baru
            user = User.objects.create_user(username=username, password=password, email=email)
            
            # Buat UserProfile
            UserProfile.objects.create(user=user, role=role)

            return JsonResponse({'status': 'success', 'message': 'Registrasi berhasil! Silakan login.'})
        except json.JSONDecodeError:
             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # PENTING: Gunakan alias auth_login
                auth_login(request, user)
                
                response = JsonResponse({
                    'status': 'success',
                    'message': 'Login berhasil!',
                    'redirect_url': '/' 
                })
                
                response.set_cookie('user_firstname', user.first_name or user.username, max_age=86400) 
                return response
            else:
                return JsonResponse({'status': 'error', 'message': 'Username atau password salah.'}, status=400)
        except json.JSONDecodeError:
             return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


@csrf_exempt
def logout_api(request):
    if request.method == 'POST':
        # PENTING: Gunakan alias auth_logout
        auth_logout(request)
        
        response = JsonResponse({'status': 'success', 'message': 'Logout berhasil.', 'redirect_url': reverse('authentication:login_page')})
        response.delete_cookie('user_firstname')
        return response

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


# ==============================================================================
# BAGIAN 3: Views API Khusus untuk FLUTTER (Mengembalikan Role & Cookie Session)
# ==============================================================================
@csrf_exempt
def flutter_login_api(request):
    if request.method != 'POST':
         return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"status": False, "message": "Username atau password salah."}, status=401)

    # Login session
    auth_login(request, user)

    # Ambil ROLE
    try:
        role = user.userprofile.role
    except:
        role = "user"

    response = JsonResponse({
        "status": True,
        "message": "Login berhasil!",
        "username": user.username,
        "role": role
    })

    response.set_cookie(
        key="sessionid",
        value=request.session.session_key,
        httponly=True,
        samesite="None",   # jika Flutter Web → "None"
        secure=True      # jika HTTPS → True
    )

    return response



@csrf_exempt
def flutter_register_api(request):
    """
    API Register khusus untuk Flutter.
    Menerima JSON: {"username": "...", "password": "...", "email": "...", "role": "..."}
    Wajib menerima 'role' agar UserProfile bisa dibuat.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password') 
            email = data.get('email')
            role = data.get('role') # Wajib ada

            # Validasi dasar
            if not all([username, password, email, role]):
                return JsonResponse({'status': False, 'message': 'Semua field (username, password, email, role) harus diisi.'}, status=400)

            # Validasi role
            if role not in ['user', 'penyedia']:
                 return JsonResponse({'status': False, 'message': 'Role tidak valid.'}, status=400)

            # Cek username tersedia
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username sudah digunakan."
                }, status=400)
            
            # 1. Buat User Django standar
            user = User.objects.create_user(username=username, password=password, email=email)
            
            # 2. PENTING: Buat UserProfile untuk menyimpan Role
            UserProfile.objects.create(user=user, role=role)
            
            return JsonResponse({
                "status": True,
                "message": "Registrasi berhasil!",
                "username": user.username,
                "role": role
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Format JSON tidak valid'}, status=400)
        except Exception as e:
            # Tangkap error lain, misal error database
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    
    else:
        return JsonResponse({"status": False, "message": "Metode tidak diizinkan."}, status=405)


@csrf_exempt
def flutter_logout_api(request):
    """API Logout khusus untuk Flutter."""
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            # PENTING: Gunakan alias auth_logout
            auth_logout(request)
            return JsonResponse({
                "status": True,
                "message": f"Sampai jumpa, {username}!"
            }, status=200)
        else:
             return JsonResponse({"status": False, "message": "Anda belum login (Sesi tidak ditemukan)."}, status=401)
    return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)