# booking/urls.py
from django.urls import path
from . import views

app_name = 'booking_lapangan'

urlpatterns = [
    path('', views.booking_dashboard_view, name='booking_dashboard'),
    path('list/', views.booking_list_view, name='booking_list'), # Daftar lapangan untuk dibooking
    path('create/', views.booking_create_view, name='booking_create'),
    path('update/<int:id>/', views.update_booking_view, name='booking_update'),
    path('cancel/<int:id>/', views.cancel_booking_view, name='booking_cancel'),
    # Anda mungkin butuh path untuk riwayat booking
    # path('history/', views.booking_history_view, name='booking_history'),
]