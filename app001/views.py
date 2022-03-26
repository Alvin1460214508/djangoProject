from django.shortcuts import render, HttpResponse

'''写函数'''


# Create your views here.
def index(request):
    return HttpResponse("欢迎使用")

def userlist(request):

    # 根据app的注册顺序，逐一在其templates文件夹中找对应的文件
    return render(request, "user_list.html")