from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from django.views import View
from markdown import markdown
from pyquery import PyQuery
#models
from app01.models import Cover,Articles,Tags
#随机包
import random

class AddArticleForm(forms.Form):
    #必填字段-文章标题，文章内容-注意必须和前端传过来的名字一直
    #为空验证
    title = forms.CharField(error_messages={'required':'请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False) #该字段不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False) #如果前端传过来，那么会添加

    # 全局钩子-如果有就存在，没有就在self.clean_data去除掉
    # 校验分类和文章密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    #abstract的局部钩子
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        #用户没有填写,截取
        #获取正文
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:30]
            return abstract

    #cover_id的局部钩子
    def clean_cover_id(self):
        cover_id = self.cleaned_data.get('cover_id')
        if cover_id:
            return cover_id
        #如果有选择呢
        cover_dict_list = Cover.objects.all().values('nid') #转换为字典对象了
        cover_id = random.choice(cover_dict_list)['nid']
        return cover_id

class ArticleView(View):
    def post(self, request):
        res={
            'msg':'文章发布成功',
            'code':200,
            'data':None
        }
        data = request.data #取出数据
        data['status'] = 1
        form = AddArticleForm(data)
        #表单校验通过
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            res['code'] = 401
            return JsonResponse(res)
        form.cleaned_data['source'] = '陈俊亦个人博客'
        form.cleaned_data['auther'] = '陈俊亦'
        #表单通过-->**表示解构
        article_obj = Articles.objects.create(**form.cleaned_data)
        #标签三种状态：1、全是数字 2、数字加自己写 3、什么都没有 4、如果自己标签有数字呢？
        tags = data.get('tags')
        for tag in tags:
            if tag.isdigit():
                article_obj.tag.add(tag)
            else:#多对多关联
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj)

        res['data'] = article_obj.nid
        return JsonResponse(res)