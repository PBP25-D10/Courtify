from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    
    path('login/', views.login_page_view, name='login_page'),
    path('register/', views.register_page_view, name='register_page'),
    path('logout/', views.logout_page_view, name='logout'),
    path('login/', views.login_page_view, name='login'),
    path('register/', views.register_page_view, name='register'),
    path('logout/', views.logout_page_view, name='logout'),

    path('api/register/', views.register_api, name='api_register'),
    path('api/login/', views.login_api, name='api_login'),
    path('api/logout/', views.logout_api, name='api_logout'),

    path('api/flutter/login/', views.flutter_login_api, name='flutter_login_api'),
    path('api/flutter/register/', views.flutter_register_api, name='flutter_register_api'),
    path('api/flutter/logout/', views.flutter_logout_api, name='flutter_logout_api'),

    path('api/flutter/auth/login/', views.flutter_auth_login_api, name='flutter_auth_login_api'),
    path('api/flutter/auth/register/', views.flutter_auth_register_api, name='flutter_auth_register_api'),
    path('api/flutter/auth/logout/', views.flutter_auth_logout_api, name='flutter_auth_logout_api'),
    path('api/flutter/auth/me/', views.flutter_auth_me_api, name='flutter_auth_me_api'),


]
