"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from article import views
import userprofile.views
import comment.views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.article_list),
    path('list/', views.article_list, name='list'),  # 文章列表
    path('detail/<int:id>/', views.article_detail, name='detail'),  # 文章详情
    path('create/', views.article_create, name='create'),
    path('delete/<int:id>/', views.article_delete, name='delete'),
    path('update/<int:id>/', views.article_update, name='update'),
    path('login/', userprofile.views.user_login, name='login'),
    path('logout/', userprofile.views.user_logout, name='logout'),
    path('register/', userprofile.views.user_register, name='register'),
    path('post-comment/<int:article_id>/', comment.views.post_comment, name='post_comment'),
]
