# accounts/urls.py
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # URL untuk halaman utama/dashboard setelah login
    path('', views.dashboard_view, name='dashboard'),
    
    # URL untuk menampilkan form
    path('login/', views.login_page_view, name='login_page'),
    path('register/', views.register_page_view, name='register_page'),
    path('logout/', views.logout_page_view, name='logout'),
    path('login/', views.login_page_view, name='login'),
    path('register/', views.register_page_view, name='register'),
    path('logout/', views.logout_page_view, name='logout'),

    # URL API untuk AJAX
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),

    # URL API Flutter
    path('api/flutter/login/', views.flutter_login_api, name='flutter_login_api'),
    path('api/flutter/register/', views.flutter_register_api, name='flutter_register_api'),
    path('api/flutter/logout/', views.flutter_logout_api, name='flutter_logout_api'),


]