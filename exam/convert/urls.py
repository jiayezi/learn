from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('modify_file/<int:file_id>/', views.modify_file, name='modify_file'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
]
