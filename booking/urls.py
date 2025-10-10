from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list_view, name='booking_list'),
    path('create/', views.booking_create_view, name='booking_create'),
    path('<int:pk>/cancel/', views.cancel_booking_view, name='booking_cancel'),
    path('<int:pk>/update/', views.update_booking_view, name='booking_update'),
]
