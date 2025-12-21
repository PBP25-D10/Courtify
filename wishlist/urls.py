from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list_view, name='wishlist_list'),
    path('add/<uuid:lapangan_id>/', views.wishlist_add_view, name='wishlist_add'),
    path('delete/<int:wishlist_id>/', views.wishlist_delete_view, name='wishlist_delete'),
    path('check/<uuid:lapangan_id>/', views.wishlist_check_view, name='wishlist_check'),

    # API endpoints (Flutter)
    path('api/list/', views.wishlist_api_list, name='wishlist_api_list'),
    path('api/toggle/<uuid:lapangan_id>/', views.wishlist_api_toggle, name='wishlist_api_toggle'),
    path('api/delete/<int:wishlist_id>/', views.wishlist_api_delete, name='wishlist_api_delete'),
    path('api/check/<uuid:lapangan_id>/', views.wishlist_api_check, name='wishlist_api_check'),
]
