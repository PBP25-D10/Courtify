# accounts/urls.py
from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # URL untuk halaman utama/dashboard setelah login
    path('', views.dashboard_view, name='dashboard'),
    
    # URL untuk menampilkan form
    path('login/', views.login_page_view, name='login'),
    path('register/', views.register_page_view, name='register'),
    path('logout/', views.logout_page_view, name='logout'),

    # URL API untuk AJAX
    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),


]