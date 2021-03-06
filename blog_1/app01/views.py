from threading import local
from unicodedata import category
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app01.utils.random_code import random_code
# 引入auth表接口
from django.contrib import auth
from app01.models import Articles,Tags,Cover


# 登录页面
def login(request):
    return render(request, 'login.html')

def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-create_date')
    qianduan_list = article_list.filter(category = 1).order_by('-create_date')[0:6]
    houduan_list = article_list.filter(category = 2).order_by('-create_date')[0:6]
    return render(request, 'index.html', locals())

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

#个人中心
def backend(request):
    if not request.user.username:
        #没有登录
        return redirect('/')
    return render(request,'backend/backend.html',{'request':request})

#个人中心-添加文章
def add_article(request):
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    
    category_list = Articles.category_choice
    return render(request,'backend/add_article.html',locals())

#后台修改头像
def edit_avatar(request):
    return render(request,'backend/edit_avatar.html',locals())
#后台修改密码
def reset_password(request):
    return render(request,'backend/reset_password.html',locals())
#后台完善信息


#后台编辑文章
def edit_article(request,nid):
    article_obj = Articles.objects.get(nid=nid)
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    category_list = Articles.category_choice

    return render(request,'backend/edit_article.html',locals())
