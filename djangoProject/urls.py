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
from django.views.generic import TemplateView

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
    path('dikwp/ships', views.dikwpships),
    path('dikwp/searchnodes', views.searchFindNodes),
    path('dikwp/searchships', views.searchFindShips),

    # Vue测试
    path('add_book/', views.add_book),
    path('show_books/', views.show_books),
    path('vue/', TemplateView.as_view(template_name="index.html")),

    # neomodel_CURD
    path('add_person/', views.addPerson),
    path('add_movie/', views.addMovie),
    path('show_person/', views.show_person),
    path('show_movie/', views.show_movie),
    path('show_specific_person/', views.showSpecificPerson),
    path('show_specific_movie/', views.showSpecificMovie),
    path('isconnect/', views.oneConnectAnother),
    path('delete_person/', views.deletePerson),
    path('delete_movie/', views.deleteMovie),
    path('delete_country/', views.deleteCountry),
]
