# booking/urls.py

from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('dashboard/', views.booking_dashboard_view, name='booking_dashboard'),
    path('list/', views.booking_list_view, name='booking_list'),
    path('create/', views.booking_create_view, name='booking_create'),
    path('update/<int:pk>/', views.update_booking_view, name='update_booking'),
    path('cancel/<int:pk>/', views.cancel_booking_view, name='cancel_booking'),
    path('my-bookings/', views.booking_user_list_view, name='booking_user_list'),

]
