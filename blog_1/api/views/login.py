from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django import forms
from app01.models import UserInfo,Avatars
# 引入auth表接口
from django.contrib import auth
from django.views import View
import random


# 登录失败的可复用代码
def clean_form(form):
    # 验证不通过
    err_dict: dict = form.errors
    # 拿到所有错误的字段名字，只拿到第一个字段
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg


# base验证表单类
class LoginBaseForm(forms.Form):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 为了拿到session的验证码，重写__init__方法
    def __init__(self, *args, **kwargs):
        # 做自己的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 局部钩子-验证码
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code.upper() != self.request.session.get('valid_code').upper():
            self.add_error("code", '验证码输入错误')
        return self.cleaned_data

# 创建forms.Form类,#登录的字段验证函数
class LoginForm(LoginBaseForm):

    # 全局钩子
    def clean(self):  # 全局前端传过来的dict
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        code = self.cleaned_data.get('code')

        user = auth.authenticate(username=name, password=pwd)
        if not user:  # 校验不通过
            # raise ValidationError('用户名或密码错误')
            self.add_error('pwd', '用户名或密码错误')
            return self.cleaned_data
        # 把用户对象放到cleaned_data中
        self.cleaned_data['user'] = user

        return self.cleaned_data


# 注册表单的验证
class SignForm(LoginBaseForm):
    re_pwd = forms.CharField(error_messages={'required': '请输入重复密码'})

    # 定义全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        code = self.cleaned_data.get('code')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '已存在该用户名')
        return self.cleaned_data


# CBV的模式开发视图函数
class LoginView(View):
    def post(self, request):
        res = {
            'code': 404,
            'msg': '登录成功！',
            'self': None,
        }
        # 把前端传来的data
        form = LoginForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 这里写登录操作
        user = form.cleaned_data.get('user')
        auth.login(request, user)

        # 都正确返回给前端
        res['code'] = 20000
        return JsonResponse(res)

class SingView(View):
    def post(self,request):
        res = {
            'code': 404,
            'msg': '注册成功！',
            'self': None,
        }
        # 开始判断
        form = SignForm(request.data, request=request)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 写验证成功的代码
        name = request.data.get('name')
        pwd = request.data.get('pwd')
        user = UserInfo.objects.create_user(username=name, password=pwd)
        # 随机选择头像
        avatar_lis = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_lis)
        user.save()
        # 注册之后直接登录
        auth.login(request, user)
        res['code'] = 20000
        return JsonResponse(res)
