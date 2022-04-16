from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect

from django.db import transaction

from app001 import models

import json
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# neo4j的import
import logging
import sys

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from app001.models import Person, Country, Book, Movie

'''写函数'''


# Create your views here.
# 初始学习网页
def index(request):
    return HttpResponse("欢迎使用")


# render返回一个网页
def userlist(request):
    # 根据app的注册顺序，逐一在其templates文件夹中找对应的文件
    return render(request, "user_list.html")


# render返回一个网页，附带参数
def tpl(request):
    name = "jieke"
    roles = ["guanliyaun", "CO"]  # 列表，不分顺序
    user_info = {"name": "jieke", "salary": 10933, 'role': "CTO"}  # 字典（一一对应）
    data_list = [
        {"name": "jieke", "salary": 10933, 'role': "CTO"},
        {"name": "jiewah", "salary": 12333, 'role': "CFO"},
        {"name": "gergke", "salary": 5093, 'role': "CEO"}
    ]

    return render(request, 'tpl.html', {"n1": name, "n2": roles, "n3": user_info, "n4": data_list})


# 向第三方网站请求数据（当前链接失效）
def news(request):
    # 可以用字典列表等定义新闻发出
    # 也可以向第三方网站发请求
    import requests
    res = requests.get("https://www.chinaunicom.com/api/article/NewsByIndex/2/2022/1/news")
    data_list = res.json()
    print(data_list)

    return render(request, 'news.html')


# GET POST 重定向传值
def something(request):
    """请求"""
    # 获取请求的方式有GET/POST
    print(request.method)

    # 通过URL传递值  /something/?n1=123&n2=99
    print(request.GET)

    # 在请求体中提交数据用POST
    # GET请求放在明面上，POST封装在一个请求体，表面看不到
    print(request.POST)

    """响应"""
    # HttpResponse将字符串内容返回
    # return HttpResponse("返回内容")

    # render返回一个页面，读取+渲染变成字符串返回给浏览器

    """返回还可以返回一个网址页面————重定向"""
    return redirect("https://www.chinaunicom.com/news/list202201.html")


# 登录验证密码
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    # else: 　
    # 不是GET就是POST，所以按流程走到这里，不需要这个else

    # GET是初次登录
    # 如果是POST请求，就说明是提交上来的表单，获取用户提交的数据
    print(request.POST)
    # 拿到表单里的单项的名字对应的数据，user和pwd是名字（name）
    username = request.POST.get("user")
    password = request.POST.get("pwd")
    print(username, password)
    if username == 'root' and password == "123":
        # return HttpResponse("登录成功")
        return redirect("https://www.baidu.com/")

    # else:
    # 最后的一个判断，作为兜底其实也不需要判断，执行即可
    # return HttpResponse("登录失败")
    return render(request, 'login.html', {"error_msg": "用户名或密码错误"})


# django操作mysql数据
def orm_test(request):
    # 测试ORM操作表格数据

    """新建"""
    # models.Department.objects.create(title="销售部")
    # models.Department.objects.create(title="IT部")
    # models.Department.objects.create(title="运营部")
    # models.Department.objects.create(title="HR部")
    # models.UserInfo.objects.create(name="jieke", password="234")
    # models.UserInfo.objects.create(name="wangke", password="432")

    """获取数据"""
    # 获取的是QuerySet类型的数据，列表型，只不过是一行一行的

    # 全选
    # data_queryset_list = models.UserInfo.objects.all()
    # for obj in data_queryset_list:
    #     print(obj.id, obj.name, obj.password, obj.age)

    # 筛选，first指选出来的数据的第一行，这样就不用再遍历寻找了
    # data_list = models.UserInfo.objects.filter(id=1).first()
    # print(data_list.id, data_list.age)

    """删除"""
    """加筛选条件再加操作"""

    # filter作为筛选器，之后跟delete操作
    # models.UserInfo.objects.filter(id=2).delete()

    # all是全选，之后跟delete操作
    # models.Department.objects.all().delete()

    """修改、更新数据"""
    # 先找到数据，再更新

    # models.UserInfo.objects.all().update(password=9999)
    # models.UserInfo.objects.filter(id=1).update(age=99)

    return HttpResponse("成功")


"""案例——用户管理"""


# 展示用户列表
def info_list(request):
    # 1. 获取数据库中所有用户信息
    # [用户1信息，用户2信息，用户3信息]
    date_list = models.UserInfo.objects.all()
    print(date_list)

    return render(request, 'info.html', {"info_list": date_list})


# 添加用户
# get看到页面输入内容
# post提交写入到数据库
def info_add(request):
    if request.method == "GET":
        return render(request, 'info_add.html')

    # 获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")

    # 把数据添加到数据库
    models.UserInfo.objects.create(name=user, password=pwd, age=age)

    # return HttpResponse('OK')
    # 添加成功的时候要跳转到列表展示
    return redirect("/info/list")


"""Neo4j操作"""


# Neo4j测试
def neo_crud(request):
    return HttpResponse("OK")


# 节点操作——增删改查测试
def dikwp(request):
    """创建sam"""
    """
    sam = Person(
        name='sam',
        age=23,
        people="汉族",
        sex='M',
        likes=['play football', 'read book', "玩桌游"],
        dislikes=["早起", 'practise']
    ) 
    sam.save()
    sam.country.connect(Country.nodes.get(code='US'))
    """
    try:
        if Person.nodes.get(name='tim'):
            # 获取节点
            tim = Person.nodes.get(name='tim')

            # 更新节点
            tim.age = 23
            tim.people = "汉族"
            tim.sex = 'M'
            tim.likes = ['play football', 'read book', "玩桌游"],
            tim.dislikes = ["早起", 'practise']

            # 保存节点
            tim.save()

            # 刷新节点
            tim.refresh()

            # 验证、操作节点
            print(tim.sex)
    # except Exception as es:
    #     print("youle")
    finally:
        return HttpResponse("节点操作有问题")

    return HttpResponse("Neo4j的增删改查测试完成")


# 节点间关系的操作
def dikwpships(request):
    # 获取、创建节点
    jackWang = Person(name='Jack', age=33)
    American = Country(code='US', countryName='American')
    littleT = Person.nodes.get(name='tim')

    # 保存、更新节点
    jackWang.save()
    American.save()

    # 创建节点间关系实例
    jackWang.country.connect(American)
    littleT.country.connect(American)

    # 验证关系操作
    if jackWang.country.is_connected(American):
        print("Jack's from American")

    if littleT.country.is_connected(American):
        print("tim's from American")

    return HttpResponse("关系的链接")


# 查找节点
def searchFindNodes(request):
    # # Return all nodes
    # all_nodes = Person.nodes.all()
    #
    # print(all_nodes)
    #
    # # Returns Person by Person.name=='Jim' or raises neomodel.DoesNotExist if no match
    # jim = Person.nodes.get(name='Jim')
    # print(jim.age)
    #
    # # Will return None unless "bob" exists
    # someone = Person.nodes.get_or_none(name='bob')
    #
    # print("Bob is {0}".format(someone))
    #
    # # Will return the first Person node with the name bob. This raises neomodel.DoesNotExist if there's no match.
    # """someone = Person.nodes.first(name='bob')
    # print("first Bob is {0}", someone)"""
    # # Will return the first Person node with the name bob or None if there's no match
    # someone = Person.nodes.first_or_none(name='bob')
    # print("first none Bob is {0}".format(someone))
    # # Return set of nodes
    # # 双下划线之后再跟gt表示大于
    # people = Person.nodes.filter(age__gt=3)
    # # 条件查找特定的nodes
    # print("people is {0}".format(people))

    return HttpResponse('find_nodes OK')


# 查找关系
def searchFindShips(request):
    # # 查询两个节点并提取
    # # germany = Country(code='DE').save()
    # germany = Country.nodes.get(code='DE')
    # jim = Person.nodes.get(name='Jim')
    #
    # # jim.country.connect(germany)
    #
    # # 看看两个节点之间有没有关系
    # if jim.country.is_connected(germany):
    #     print("Jim's from Germany")
    #
    # # 遍历德国这个节点，看看有哪些个人是德国人
    # for p in germany.inhabitant.all():
    #     print(p.name)  # Jim
    #
    # # 数数看有多少个人是德国人
    # countger = len(germany.inhabitant)  # 1
    # print(countger)
    #
    # # 找到一个叫jim的德国人
    # # Find people called 'Jim' in germany
    # if germany.inhabitant.search(name='Jim'):
    #     print("There is a Jim who comes from germany")
    #
    # # 找到所有叫jim的德国人
    # # Find all the people called in germany except 'Jim'
    # if germany.inhabitant.exclude(name='Jim'):
    #     print("Many Jim are germany")
    #
    # # Remove Jim's country relationship with Germany
    # jim.country
    # usa = Country(code='US').save()
    # jim.country.connect(usa)
    # jim.country.connect(germany)
    #
    # # Remove all of Jim's country relationships
    # jim.country.disconnect_all()
    #
    # jim.country.connect(usa)
    # # Replace Jim's country relationship with a new one
    # jim.country.replace(germany)

    return HttpResponse('find_relationship OK')


# addPerson接受一个post请求，往数据库里添加一条person数据
@require_http_methods(["POST"])
def addPerson(request):
    response = {}
    try:
        someone = Person(
            name=request.POST.get('book_name'),
            age=request.POST.get('book_name'),
            people=request.POST.get('book_name'),
            sex=request.POST.get('book_name'),
            likes=request.POST.get(''),
            dislikes=request.POST.get('')
        )
        someone.save()
        someone.country.connect(request.POST.get('country'))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# addCountry接受一个post请求，往数据库里添加一条country数据
@require_http_methods(["POST"])
def addCountry(request):
    response = {}
    try:
        oneCountry = Country(
            code=request.POST.get('book_name'),
            countryName=request.POST.get('book_name')
        )
        oneCountry.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# addMovie接受一个post请求，往数据库里添加一条movie数据
@require_http_methods(["POST"])
def addMovie(request):
    response = {}
    try:
        oneMovie = Movie(
            title=request.POST.get('book_name'),
            releasedTime=request.POST.get('book_name'),
            tags=request.POST.get('book_name'),
            score=request.POST.get('book_name'),
        )
        oneMovie.save()
        oneMovie.actors.connect(request.POST.get('actors'), {'isLeader': request.POST.get('isLeader')})
        oneMovie.director.connect(request.POST.get('director'))
        oneMovie.writer.connect(request.POST.get('writer'))
        oneMovie.producer.connect(request.POST.get('producer'))
        oneMovie.country.connect(request.POST.get('country'))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 查找所有的人物信息（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def show_person(request):
    response = {}
    try:
        persons = Person.nodes.all()
        response['list'] = json.loads(serializers.serialize("json", persons))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 查找所有的电影信息（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def show_movie(request):
    response = {}
    try:
        movies = Movie.nodes.all()
        response['list'] = json.loads(serializers.serialize("json", movies))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 查找特定的人物具体信息（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def showSpecificPerson(request):
    response = {}
    try:
        certainOne = Person.nodes.get_or_none(name=request.GET.get('name'))
        response['list'] = json.loads(serializers.serialize("json", certainOne))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 查找特定的电影具体信息（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def showSpecificMovie(request):
    response = {}
    try:
        certainMovie = Person.nodes.get_or_none(title=request.GET.get('title'))
        response['list'] = json.loads(serializers.serialize("json", certainMovie))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 比较电影和人之间的关系（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def oneConnectAnother(request):
    response = {}
    try:
        one = Person.GET.get(name=request.GET.get('person_name'))
        another = Movie.GET.get(name=request.GET.get('movie_name'))
        response['isActor'] = another.actors.is_connected(one)
        response['isDirector'] = another.director.is_connected(one)
        response['isWriter'] = another.writer.is_connected(one)
        response['isProducer'] = another.producer.is_connected(one)
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 删除特定的人（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def deletePerson(request):
    response = {}
    try:
        certainOne = Person.nodes.get_or_none(name=request.GET.get('name'))
        certainOne.delete()
        certainOne.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 删除特定的电影（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def deleteMovie(request):
    response = {}
    try:
        certainMovie = Movie.nodes.get_or_none(title=request.GET.get('title'))
        certainMovie.delete()
        certainMovie.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 删除特定的国家（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def deleteCountry(request):
    response = {}
    try:
        certainCountry = Country.nodes.get_or_none(countryName=request.GET.get('countryName'))
        certainCountry.delete()
        certainCountry.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


"""测试用添加查找书籍"""


# show_books返回所有的书籍列表（通过JsonResponse返回能被前端识别的json格式数据）
@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# add_book接受一个get请求，往数据库里添加一条book数据
@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)