# main/urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.landing_page_view, name='landing_page'),
    # URLs untuk Artikel (News)
    path('artikel/', views.news_list_view, name='news_list'),
    path('artikel/tambah/', views.news_create_view, name='news_create'),
    path('artikel/edit/<int:id>/', views.news_edit_view, name='news_edit'),
    path('artikel/hapus/<int:id>/', views.news_delete_view, name='news_delete'),

    # URLs untuk Iklan
    path('iklan/', views.iklan_list_view, name='iklan_list'),
    path('iklan/tambah/', views.iklan_create_view, name='iklan_create'),
    path('iklan/edit/<int:id>/', views.iklan_edit_view, name='iklan_edit'),
    path('iklan/hapus/<int:id>/', views.iklan_delete_view, name='iklan_delete'),

    # URLs untuk Wishlist
    path('wishlist/', views.wishlist_list_view, name='wishlist_list'),
    path('wishlist/tambah/', views.wishlist_create_view, name='wishlist_create'),
    path('wishlist/hapus/<int:id>/', views.wishlist_delete_view, name='wishlist_delete'),
]