from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from app01.utils.random_code import random_code
import json


def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')

#获取图片验证码
def get_code(request):
    data , valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)

#登录页面
def login(request):
    if request.method == 'POST':
        data = request.data
        valid_code:str = request.session.get('valid_code')
        if valid_code.upper() == data.get('code').upper():
            print('验证码输入正确')
        else:
            print('验证码输入cuowu')
        return JsonResponse(data)
    return render(request,'login.html')

#注册界面
def sign(request):
    return render(request,'sign.html')
