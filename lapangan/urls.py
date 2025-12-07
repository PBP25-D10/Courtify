from django.urls import path
from . import views

app_name = 'manajemen_lapangan'

urlpatterns = [
    path('', views.manajemen_dashboard_view, name='manajemen_dashboard'),
    path('lapangan/', views.lapangan_list_view, name='lapangan_list_owner'),
    path('lapangan/create/', views.lapangan_create_view, name='lapangan_create'),
    path('lapangan/edit/<uuid:id_lapangan>/', views.lapangan_edit_view, name='lapangan_edit'),
    path('lapangan/delete/<uuid:id_lapangan>/', views.lapangan_delete_view, name='lapangan_delete'),
    
    path('api/list/', views.flutter_api_list_lapangan, name='api_list_lapangan'),
    path('api/create/', views.flutter_api_create_lapangan, name='api_create_lapangan'),
    path('api/update/<uuid:id_lapangan>/', views.flutter_api_update_lapangan, name='api_update_lapangan'),
    path('api/delete/<uuid:id_lapangan>/', views.flutter_api_delete_lapangan, name='api_delete_lapangan'),
    path('lapangan/delete/<uuid:id_lapangan>/', views.lapangan_delete_view, name='lapangan_delete'),
    path('api/upload-foto/<uuid:id_lapangan>/', views.flutter_api_upload_foto_lapangan, name='flutter_upload_foto_lapangan'),
]
