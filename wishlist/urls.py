from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list_view, name='wishlist_list'),
    path('add/<uuid:lapangan_id>/', views.wishlist_add_view, name='wishlist_add'),
    path('delete/<int:wishlist_id>/', views.wishlist_delete_view, name='wishlist_delete'),
]
