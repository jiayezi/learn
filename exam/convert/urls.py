from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('convert_page/', views.convert_page, name='convert_page'),
    path('rank_page/', views.rank_page, name='rank_page'),
    path('sum_page/', views.sum_page, name='sum_page'),
    path('download_file/', views.download_file, name='download_file'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('config/', views.config_list, name='config_list'),
    path('config/create/', views.create_config, name='create_config'),
    path('config/modify/<int:config_id>/', views.modify_config, name='modify_config'),
    path('config/delete/<int:config_id>/', views.delete_config, name='delete_config'),
]
