# djangoProject
djangoFirst

url -> 函数
首先要新建一个app，类似于项目中的细分单元

再在setting.py里的INSTALLED_APPS选项里进行注册

url写在url.py

        要说清楚网址的后缀和调用的是哪一个视图函数
函数写在views.py

        函数返回文字用HttpResponse

        返回html文件，即使用模板则需要在app的templates文件夹里新建好模板html文件，在views.py里用render返回
        
        返回静态文件，比如图片、CSS、JS文件，就要新建一个文件夹里放置这些文件
        
        在文件头里加{% load static %}，之后整个文件的静态资源引用就可以直接写{% static 'XXX' %}

模板语法：写一些占位符，用数据去代替占位符
    {{}} 两个大括号表示占位符，里面括的是变量
语句

    循环语句
        {% for k,v in n3.items %}   <!--keys,values获取键和值-->
            <li>{{ k }} = {{ v }}</li>
        {% endfor %}

    条件语句
        {% if n1 == "jieke" %}
            <h1>hhhhh</h1>
        {% else %}
            <h1>wwwww</h1>
        {% endif %}
Django的流程（左边的圈代表用户的浏览器）
![](app001/static/img/djangoFlow.png)

请求和响应 

    def userlist(request):
        # 根据app的注册顺序，逐一在其templates文件夹中找对应的文件
        return render(request, "user_list.html")
request作为一个对象，封装了用户发送过来的所有数据
示例函数

    def something(request):
请求

    # 获取请求的方式有GET/POST
    print(request.method)

    # 通过URL传递值  /something/?n1=123&n2=99
    print(request.GET)

    # 在请求体中提交数据用POST
    # GET请求放在明面上，POST封装在一个请求体，表面看不到
    print(request.POST)

响应

    # HttpResponse将字符串内容返回
    #return HttpResponse("返回内容")

    # render返回一个页面，读取+渲染变成字符串返回给浏览器
    
    '''返回还可以返回一个网址页面————重定向'''
    return redirect("http://www.chinaunicom.com/news/list202201.html")

做一个用户登录的小案例
login
链接数据库
    
1. 用pymysql
![](app001/static/img/python操作MySQL.png)
2. Django内部的ORM框架操作数据库
![](app001/static/img/ORM的作用.png)
    
ORM

功能

    1. 对表格增删改查（不写SQL语句）
        不能创建数据库
    2. 对表中数据增删改查

方法
1. 创建数据库
2. 在setting.py里做配置，用Django链接数据库
![](app001/static/img/settingSQL.png)
3. 配置models.py，用Django对表格进行增删改查

    建表（增删改查表）
    ![](app001/static/img/修改models文件建表.png)
    执行命令，使得数据库中真正建表成功


        python.exe manage.py makemigrations
        python.exe manage.py migrate

4. 对表中数据进行操作


Python Neomodel
1. 先注册app，放在自己的app之前
2. 在setting.py配置数据库地址

    
    from neomodel import config
    config.DATABASE_URL = 'bolt://neo4j:123456@localhost:7687/dikwp'

    'neo4j'是链接数据库的用户名
    '123456'是进数据库的密码
    localhost:7687是IP和端口，要看Neo4j的浏览器里显示的
![img.png](img.png)


    dikwp是自己建的数据库的名字，加上之后可以在自己想要的地方准确建立节点

3. 第一大步骤——链接就完成了
4. 开始定义节点和关系
5. 提交，就是教程上的应用约束和索引


    python.exe manage.py install_labels

6. 对节点数据的增删改查


    jim = Person(name='Jim', age=3).save() # Create
    jim.age = 4
    jim.save() # Update, (with validation)带校验的更新
    jim.delete()
    jim.refresh() # reload properties from the database  删除之后不能刷新
    jim.id # neo4j internal id内部ID

在建好models之后运行


    python.exe manage.py install_labels