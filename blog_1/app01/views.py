from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


#登录页面
def login(request):
    return render(request,'login.html')

#注册界面
def sign(request):
    return render(request,'sign.html')
