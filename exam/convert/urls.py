from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('convert_page/', views.convert_page, name='convert_page'),
    path('rank_page/', views.rank_page, name='rank_page'),
    path('sum_page/', views.sum_page, name='sum_page'),
    path('download_file/<int:file_id>/', views.download_file, name='download_file'),
]
