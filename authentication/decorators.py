from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('authentication:login_page')

            try:
                user_role = request.user.userprofile.role
                if user_role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('authentication:dashboard')
            except AttributeError:
                return redirect('authentication:dashboard')

        return wrapper
    return decorator


def is_penyedia(user):
    return user.is_authenticated and user.userprofile.role == 'penyedia'

def is_user(user):
    return user.is_authenticated and user.userprofile.role == 'user'

penyedia_required = user_passes_test(is_penyedia, login_url='/auth/login/')
user_required = user_passes_test(is_user, login_url='/auth/login/')
