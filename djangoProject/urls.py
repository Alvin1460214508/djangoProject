"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from app001 import views

# url和函数的对应关系

urlpatterns = [
    path('admin/', admin.site.urls),

    # 测试
    path('index/', views.index),
    path('user/list', views.userlist),
    path('tpl/', views.tpl),

    # 请求与响应
    path('news/', views.news),
    path('some/', views.something),

    # 案例——用户登录
    path('login/', views.login),

    # 数据库操作
    path('orm/', views.orm_test),

    # 案例——用户管理
    path('info/list', views.info_list),  # 展示用户列表
    path('info/add', views.info_add),    # 添加用户
    path('dikwp/crud', views.dikwp),
    path('dikwp/searchnodes', views.searfind_nodes),
    path('dikwp/searchships', views.searfind_ships),
]
