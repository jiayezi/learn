from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_file, name="upload_file"),
    path("index/", views.index, name="index"),
    path('convert_page/', views.convert_page, name='convert_page'),
    path('rank_page/', views.rank_page, name='rank_page'),
    path('sum_page/', views.sum_page, name='sum_page'),
    path('download_file/', views.download_file, name='download_file'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
