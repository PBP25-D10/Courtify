from django.urls import path, include
from . import views

app_name = 'booking'

urlpatterns = [
    path('dashboard/', views.booking_dashboard_view, name='booking_dashboard'),
    path('list/', views.booking_list_view, name='booking_list'),
    path('create/<uuid:id_lapangan>/', views.booking_create_view, name='booking_create'),
    path('update/<int:pk>/', views.update_booking_view, name='update_booking'),
    path('cancel/<int:pk>/', views.cancel_booking_view, name='cancel_booking'),
    path('confirm/<int:pk>/', views.confirm_booking_view, name='confirm_booking'),
    path('my-bookings/', views.booking_user_list_view, name='booking_user_list'),
    path('api/booked/<uuid:lapangan_id>/<str:tanggal>/', views.get_booked_hours, name='get_booked_hours'),
    path('api/dashboard/', views.api_booking_dashboard),
    path('api/my-bookings/', views.api_booking_user_list),
    path('api/owner-bookings/', views.api_owner_bookings),
    path('api/create/<uuid:id_lapangan>/', views.api_create_booking),
    path('api/cancel/<int:booking_id>/', views.api_cancel_booking),
    path('api/flutter/bookings/', views.flutter_api_booking_list, name='flutter_booking_list'),
    path('api/flutter/bookings/owner/', views.flutter_api_owner_booking_list, name='flutter_owner_booking_list'),
    path('api/flutter/bookings/create/<uuid:id_lapangan>/', views.flutter_api_create_booking, name='flutter_create_booking'),
    path('api/flutter/bookings/cancel/<int:booking_id>/', views.flutter_api_cancel_booking, name='flutter_cancel_booking'),
    path('api/flutter/bookings/confirm/<int:booking_id>/', views.flutter_api_confirm_booking, name='flutter_confirm_booking'),
    path('api/flutter/bookings/owner/cancel/<int:booking_id>/', views.flutter_api_owner_cancel_booking, name='flutter_owner_cancel_booking'),
    path('api/flutter/booked/<uuid:lapangan_id>/<str:tanggal>/', views.flutter_api_get_booked_hours, name='flutter_get_booked_hours'),
]
