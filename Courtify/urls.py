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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('manajemen/', include('lapangan.urls')),
    path('booking/', include('booking.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('artikel/', include(('artikel.urls', 'artikel'), namespace='artikel')),
    path('', include('main.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
