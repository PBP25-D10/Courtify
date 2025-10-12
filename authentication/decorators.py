# accounts/decorators.py
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles=[]):
    """
    Decorator untuk view yang memeriksa apakah user memiliki peran yang diizinkan.
    Contoh penggunaan:
    @role_required(allowed_roles=['admin', 'penyedia'])
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Jika user tidak login, redirect ke halaman login
            if not request.user.is_authenticated:
                return redirect('authentication:login_page') # Ganti dengan nama URL login Anda

            # Cek apakah user memiliki peran yang diizinkan
            try:
                # Ambil role dari UserProfile yang terhubung
                user_role = request.user.userprofile.role
                if user_role in allowed_roles:
                    # Jika diizinkan, lanjutkan ke view asli
                    return view_func(request, *args, **kwargs)
                else:
                    # Jika tidak diizinkan, lempar error Permission Denied (403 Forbidden)
                    # atau redirect ke halaman lain
                    # raise PermissionDenied
                    return redirect('authentication:dashboard') # Redirect ke dashboard umum
            except AttributeError:
                # Handle jika user tidak punya UserProfile (seharusnya tidak terjadi)
                return redirect('authentication:dashboard') # atau halaman error

        return wrapper
    return decorator

# --- Alternatif lebih sederhana jika Anda hanya butuh 1 role per decorator ---

def is_penyedia(user):
    return user.is_authenticated and user.userprofile.role == 'penyedia'

def is_user(user):
    return user.is_authenticated and user.userprofile.role == 'user'

# Decorator yang sudah jadi, siap pakai
penyedia_required = user_passes_test(is_penyedia, login_url='/auth/login/')
user_required = user_passes_test(is_user, login_url='/auth/login/')