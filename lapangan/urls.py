# manajemen_lapangan/urls.py
from django.urls import path
from . import views

app_name = 'lapangan'

urlpatterns = [
    path('', views.lapangan_list_view, name='lapangan_list_owner'),
    path('tambah/', views.lapangan_create_view, name='lapangan_create'),    
    path('<uuid:id_lapangan>/', views.lapangan_detail_view, name='lapangan_detail'),
    path('edit/<uuid:id_lapangan>/', views.lapangan_edit_view, name='lapangan_edit'),
    path('hapus/<uuid:id_lapangan>/', views.lapangan_delete_view, name='lapangan_delete'),
    path('json/<uuid:id_lapangan>/', views.lapangan_get_json, name='lapangan_get_json')
]
