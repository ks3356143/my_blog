from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from app01.utils.random_code import random_code
#引入auth表接口
from django.contrib import auth
import json
from django import forms
#导入全部钩子异常
from django.core.exceptions import ValidationError
#登录失败的可复用代码
def clean_form(form):
    # 验证不通过
    err_dict: dict = form.errors
    # 拿到所有错误的字段名字，只拿到第一个字段
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误
    err_msg = err_dict[err_valid][0]
    return err_valid,err_msg


#创建forms.Form类,#登录的字段验证函数
class LoginForm(forms.Form):
    name = forms.CharField(error_messages={'required':'请输入用户名'})
    pwd = forms.CharField(error_messages={'required':'请输入密码'})
    code = forms.CharField(error_messages={'required':'请输入验证码'})
    #为了拿到session的验证码，重写__init__方法
    def __init__(self,*args,**kwargs):
        #做自己的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args,**kwargs)

    #局部钩子
    def clean_code(self):
        code:str = self.cleaned_data.get('code')
        valid_code:str = self.request.session.get('valid_code')
        if valid_code.upper() != code.upper():
            self.add_error('code','验证码输入错误')
        return self.cleaned_data

    #全局钩子
    def clean(self): #全局前端传过来的dict
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        code = self.cleaned_data.get('code')

        user = auth.authenticate(username=name,password=pwd)
        if not user: #校验不通过
            # raise ValidationError('用户名或密码错误')
            self.add_error('pwd','用户名或密码错误')
            return self.cleaned_data
        #把用户对象放到cleaned_data中
        self.cleaned_data['user'] = user

        return self.cleaned_data

#登录页面
def login(request):
    if request.method == 'POST':
        res = {
            'code':404,
            'msg':'登录成功！',
            'self':None,
        }
        #把前端传来的data
        form = LoginForm(request.data,request=request)
        if not form.is_valid():
            res['self'] ,res['msg'] = clean_form(form)
            return JsonResponse(res)
        #这里写登录操作
        user = form.cleaned_data.get('user')
        auth.login(request,user)

        #都正确返回给前端
        res['code'] = 20000
        return JsonResponse(res)

    return render(request,'login.html')


def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')

#获取图片验证码
def get_code(request):
    data , valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)



#注册界面
def sign(request):
    return render(request,'sign.html')
