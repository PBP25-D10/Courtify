# main/urls.py
from django.urls import path
from . import views
from .views import proxy_image, flutter_api_list_iklan, flutter_api_landing_page_iklan, flutter_api_create_iklan, flutter_api_delete_iklan, flutter_api_update_iklan

app_name = 'main'

urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),
    # URLs untuk Iklan
    path('iklan/', views.iklan_list_view, name='iklan_list'),
    path('iklan/tambah/', views.iklan_create_view, name='iklan_create'),
    path('iklan/edit/<int:id>/', views.iklan_edit_view, name='iklan_edit'),
    path('iklan/hapus/<int:id>/', views.iklan_delete_view, name='iklan_delete'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    
    path('api/iklan/list/', flutter_api_list_iklan, name='flutter_api_list_iklan'),
    path('api/iklan/landing/', flutter_api_landing_page_iklan, name='flutter_api_landing_page_iklan'),
    path('api/iklan/create/', flutter_api_create_iklan, name='flutter_api_create_iklan'),
    path('api/iklan/update/<int:id_iklan>/', flutter_api_update_iklan, name='flutter_api_update_iklan'),
    path('api/iklan/delete/<int:id_iklan>/', flutter_api_delete_iklan, name='flutter_api_delete_iklan'),
]
