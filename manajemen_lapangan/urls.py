# manajemen_lapangan/urls.py
from django.urls import path
from . import views

app_name = 'manajemen_lapangan'

urlpatterns = [
    path('', views.manajemen_dashboard_view, name='manajemen_dashboard'),
    path('lapangan/', views.lapangan_list_view, name='lapangan_list_owner'),
    path('lapangan/tambah/', views.lapangan_create_view, name='lapangan_create'),
    path('lapangan/edit/<int:id>/', views.lapangan_edit_view, name='lapangan_edit'),
    path('lapangan/hapus/<int:id>/', views.lapangan_delete_view, name='lapangan_delete'),
]