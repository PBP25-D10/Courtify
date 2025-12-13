# main/urls.py
from django.urls import path
from . import views
from .views import proxy_image, show_json_iklan

app_name = 'main'

urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),
    # URLs untuk Iklan
    path('iklan/', views.iklan_list_view, name='iklan_list'),
    path('iklan/tambah/', views.iklan_create_view, name='iklan_create'),
    path('iklan/edit/<int:id>/', views.iklan_edit_view, name='iklan_edit'),
    path('iklan/hapus/<int:id>/', views.iklan_delete_view, name='iklan_delete'),
    path('proxy-image/', proxy_image, name='proxy_image'),
    path('iklan/show-json/', show_json_iklan, name='show_json_iklan'),
]
