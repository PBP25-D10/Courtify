from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Halaman owner / web
    path('', views.news_list_view, name='news_list'),
    path('create/', views.news_create_view, name='news_create'),
    path('update/<int:pk>/', views.news_update_view, name='news_update'),
    path('delete/<int:pk>/', views.news_delete_view, name='news_delete'),

    # 🌐 Halaman publik web
    path('public/', views.news_public_list_view, name='news_public_list'),
    path('<int:pk>/', views.news_detail_view, name='news_detail'),

    # 📱 API untuk Flutter
    path('json/', views.news_list_json, name='news_json'),
    path('create-flutter/', views.create_news_flutter, name='create_news_flutter'),
    path('delete-flutter/<int:id>/', views.delete_news_flutter, name='delete_news_flutter'),
]
