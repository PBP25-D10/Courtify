from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list_view, name='news_list'),
    path('create/', views.news_create_view, name='news_create'),
    path('update/<int:pk>/', views.news_update_view, name='news_update'),
    path('delete/<int:pk>/', views.news_delete_view, name='news_delete'),
    path('public/', views.news_public_list_view, name='news_public_list'),
    path('<int:pk>/', views.news_detail_view, name='news_detail'),
]
