from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserProfile

def _get_user_role(user):
    """
    Helper untuk membaca role user secara aman.
    Jika UserProfile belum ada, fallback ke 'user'.
    """
    try:
        return user.userprofile.role
    except (AttributeError, UserProfile.DoesNotExist):
        return 'user'

def login_page_view(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/login.html')

def register_page_view(request):
    if request.user.is_authenticated:
        return redirect('authentication:dashboard')
    return render(request, 'authentication/register.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('authentication:login_page')
    return render(request, 'authentication/dashboard.html')

def logout_page_view(request):
    auth_logout(request)
    response = redirect('authentication:login_page') 
    response.delete_cookie('user_firstname')
    return response


@csrf_exempt
def register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            role = data.get('role')

            if not all([username, password, email, role]):
                return JsonResponse({'status': 'error', 'message': 'Semua field harus diisi.'}, status=400)
            
            if role not in ['user', 'penyedia']:
                return JsonResponse({'status': 'error', 'message': 'Peran tidak valid.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username sudah digunakan.'}, status=400)

            user = User.objects.create_user(username=username, password=password, email=email)
            
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
        auth_logout(request)
        
        response = JsonResponse({'status': 'success', 'message': 'Logout berhasil.', 'redirect_url': reverse('authentication:login_page')})
        response.delete_cookie('user_firstname')
        return response

    return JsonResponse({'status': 'error', 'message': 'Metode tidak diizinkan.'}, status=405)


@csrf_exempt
def flutter_login_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({"status": False, "message": "Username atau password salah."}, status=401)

        auth_login(request, user)

        try:
            role = user.userprofile.role
        except AttributeError:
            role = 'user'
        
        return JsonResponse({
            "status": True,
            "message": "Login berhasil!",
            "username": user.username,
            "role": role
        }, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Format JSON tidak valid'}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': f'Terjadi kesalahan server: {str(e)}'}, status=500)


@csrf_exempt
def flutter_register_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password') 
            email = data.get('email')
            role = data.get('role')

            if not all([username, password, email, role]):
                return JsonResponse({'status': False, 'message': 'Semua field (username, password, email, role) harus diisi.'}, status=400)

            if role not in ['user', 'penyedia']:
                 return JsonResponse({'status': False, 'message': 'Role tidak valid.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username sudah digunakan."
                }, status=400)
            
            user = User.objects.create_user(username=username, password=password, email=email)
            
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
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    
    else:
        return JsonResponse({"status": False, "message": "Metode tidak diizinkan."}, status=405)


@csrf_exempt
def flutter_logout_api(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            auth_logout(request)
            return JsonResponse({
                "status": True,
                "message": f"Sampai jumpa, {username}!"
            }, status=200)
        else:
             return JsonResponse({"status": False, "message": "Anda belum login (Sesi tidak ditemukan)."}, status=401)
    return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)


@csrf_exempt
def flutter_auth_register_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Format JSON tidak valid'}, status=400)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not all([username, password, email, role]):
        return JsonResponse({'status': False, 'message': 'Semua field (username, password, email, role) harus diisi.'}, status=400)

    if role not in ['user', 'penyedia']:
        return JsonResponse({'status': False, 'message': 'Role tidak valid.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': False, 'message': 'Username sudah digunakan.'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)

    if data.get('first_name'):
        user.first_name = data['first_name']
    if data.get('last_name'):
        user.last_name = data['last_name']
    user.save()

    UserProfile.objects.create(user=user, role=role)

    return JsonResponse({
        'status': True,
        'message': 'Registrasi berhasil!',
        'user': {
            'username': user.username,
            'email': user.email,
            'role': role,
        }
    }, status=201)


@csrf_exempt
def flutter_auth_login_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Format JSON tidak valid'}, status=400)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'status': False, 'message': 'Username dan password wajib diisi.'}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({'status': False, 'message': 'Username atau password salah.'}, status=401)

    auth_login(request, user)

    if not request.session.session_key:
        request.session.save()

    role = _get_user_role(user)

    return JsonResponse({
        'status': True,
        'message': 'Login berhasil!',
        'sessionid': request.session.session_key,
        'user': {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': role,
        }
    }, status=200)


@csrf_exempt
def flutter_auth_logout_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': False, 'message': 'Metode harus POST'}, status=405)

    if request.user.is_authenticated:
        username = request.user.username
        auth_logout(request)
        return JsonResponse({'status': True, 'message': f'Logout berhasil, sampai jumpa {username}!'})

    return JsonResponse({'status': False, 'message': 'Anda belum login.'}, status=401)


@csrf_exempt
def flutter_auth_me_api(request):
    if request.method != 'GET':
        return JsonResponse({'status': False, 'message': 'Metode harus GET'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'status': False, 'message': 'Belum login atau sesi kedaluwarsa.'}, status=401)

    role = _get_user_role(request.user)

    return JsonResponse({
        'status': True,
        'message': 'Sesi masih aktif.',
        'user': {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'role': role,
        }
    })
