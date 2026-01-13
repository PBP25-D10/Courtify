# booking/urls.py

from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    # 🏠 Dashboard Booking (halaman utama pengguna untuk melihat pesanan mereka)
    path('dashboard/', views.booking_dashboard_view, name='booking_dashboard'),

    # 📋 List semua booking (admin atau penyedia bisa melihat daftar semua pesanan)
    path('', views.booking_list_view, name='booking_list'),

    # ➕ Form untuk membuat booking baru
    path('create/', views.booking_create_view, name='booking_create'),

    # ✏️ Update/edit booking yang sudah ada
    path('<int:pk>/update/', views.update_booking_view, name='booking_update'),

    # ❌ Batalkan booking tertentu
    path('<int:pk>/cancel/', views.cancel_booking_view, name='booking_cancel'),

    # 🔍 Detail booking (opsional, bisa ditambahkan nanti)
    # path('<int:pk>/', views.booking_detail_view, name='booking_detail'),
]
