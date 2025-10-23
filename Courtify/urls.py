"""
URL configuration for Courtify project.

The `urlpatterns` list routes URLs to views. 
For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

PROJECT: Courtify
ENVIRONMENTS:
    🔹 Development → http://127.0.0.1:8000/
    🔹 Production  → https://justin-timothy-courtify.pbp.cs.ui.ac.id/

FULL URL MAP
--------------------------------------------------------
🏠 MAIN APP
    /                            → main:landing_page
    /artikel/                    → main:news_list
    /artikel/tambah/             → main:news_create
    /artikel/edit/<id>/          → main:news_edit
    /artikel/hapus/<id>/         → main:news_delete
    /iklan/                      → main:iklan_list
    /iklan/tambah/               → main:iklan_create
    /iklan/edit/<id>/            → main:iklan_edit
    /iklan/hapus/<id>/           → main:iklan_delete
    /wishlist/                   → main:wishlist_list
    /wishlist/tambah/            → main:wishlist_create
    /wishlist/hapus/<id>/        → main:wishlist_delete

🔐 AUTHENTICATION APP
    /auth/login/                 → authentication:login
    /auth/register/              → authentication:register
    /auth/profile/               → authentication:profile
    /auth/logout/                → authentication:logout

🏟️ LAPANGAN APP
    /manajemen/                  → lapangan:lapangan_list
    /manajemen/tambah/           → lapangan:lapangan_create
    /manajemen/edit/<id>/        → lapangan:lapangan_edit
    /manajemen/hapus/<id>/       → lapangan:lapangan_delete
    /manajemen/dashboard/        → lapangan:dashboard

📅 BOOKING APP
    /booking/                    → booking:booking_list
    /booking/create/             → booking:booking_create
    /booking/<pk>/update/        → booking:booking_update
    /booking/<pk>/cancel/        → booking:booking_cancel
    /booking/dashboard/          → booking:booking_dashboard

⚙️ ADMIN
    /admin/                      → Django Admin Panel
--------------------------------------------------------
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 URL untuk autentikasi (login, register, profil)
    path('auth/', include('authentication.urls')),

    # 🏟️ URL untuk manajemen lapangan (khusus penyedia)
    path('manajemen/', include('lapangan.urls')),

    # 📅 URL untuk booking
    path('booking/', include('booking.urls')),

      # URL untuk artikel
    path('artikel/', include(('artikel.urls', 'artikel'), namespace='artikel')),

    # 🏠 URL untuk fitur utama (artikel, wishlist, iklan)
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
