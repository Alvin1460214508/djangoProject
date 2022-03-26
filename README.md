# djangoProject
djangoFirst

url -> 函数
首先要新建一个app，类似于项目中的细分单元
再在setting.py里的INSTALLED_APPS选项里进行注册

url写在url.py，要说清楚网址的后缀和调用的是哪一个视图函数
函数写在views.py

        函数返回文字用HttpResponse

        返回html文件，即使用模板则需要在app的templates文件夹里新建好模板html文件，在views.py里用render返回
        
        返回静态文件，比如图片、CSS、JS文件，就要
