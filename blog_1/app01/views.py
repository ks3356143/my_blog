from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.utils.random_code import random_code
# 引入auth表接口
from django.contrib import auth
from app01.models import Articles


# 登录页面
def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html', {'request': request})

def article(request,nid):
    #找到该nid的数据
    article_query = Articles.objects.filter(nid=nid)
    print(article_query)
    if not article_query:
        return redirect('/')
    article = article_query.first()

    return render(request,'article.html',locals())

def news(request):
    return render(request, 'news.html')

# 获取图片验证码
def get_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)

# 注销界面
def logout(request):
    auth.logout(request)
    return redirect('/')

# 注册界面
def sign(request):
    return render(request, 'sign.html')

# 文章详情页面跳转
