from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
from api.views.login import clean_form
from django.views import View
from markdown import markdown
from pyquery import PyQuery
from django.db.models import F
# models
from app01.models import Cover, Articles, Tags
# 随机包
import random


class AddArticleForm(forms.Form):
    # 必填字段-文章标题，文章内容-注意必须和前端传过来的名字一致
    # 为空验证
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 该字段不进行为空验证
    cover_id = forms.IntegerField(required=False)

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)  # 如果前端传过来，那么会添加

    # 全局钩子-如果有就存在，没有就在self.clean_data去除掉
    # 校验分类和文章密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # abstract的局部钩子
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 用户没有填写,截取
        # 获取正文
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # cover_id的局部钩子
    def clean_cover_id(self):
        cover_id = self.cleaned_data.get('cover_id')
        if cover_id:
            return cover_id
        # 如果有选择呢
        cover_dict_list = Cover.objects.all().values('nid')  # 转换为字典对象了
        cover_id = random.choice(cover_dict_list)['nid']
        return cover_id

#给文章添加标签
def add_article_tags(tags,article_obj):
    for tag in tags:
            if tag.isdigit():
                article_obj.tag.add(tag)
            else:  # 多对多关联
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj)
    
class ArticleView(View):
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 200,
            'data': None
        }
        data = request.data  # 取出数据
        data['status'] = 1
        form = AddArticleForm(data)
        # 表单校验通过
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            res['code'] = 401
            return JsonResponse(res)
        form.cleaned_data['source'] = '陈俊亦个人博客'
        form.cleaned_data['auther'] = '陈俊亦'
        # 表单通过-->**表示解构
        article_obj = Articles.objects.create(**form.cleaned_data)
        # 标签三种状态：1、全是数字 2、数字加自己写 3、什么都没有 4、如果自己标签有数字呢？
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags,article_obj)

        res['data'] = article_obj.nid
        return JsonResponse(res)

    def put(self, request, nid):
        res = {
            'msg': '文章修改成功',
            'code': 200,
            'data': None
        }
        #先在数据库查一下
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '没有这篇文章'
            return JsonResponse(res)
        
        data = request.data  # 取出数据
        data['status'] = 1
        form = AddArticleForm(data)
        # 表单校验通过
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            res['code'] = 401
            return JsonResponse(res)
        form.cleaned_data['source'] = '陈俊亦个人博客'
        form.cleaned_data['auther'] = '陈俊亦'
        # 表单修改
        article_query.update(**form.cleaned_data)
        # 获取标签
        tags = data.get('tags')
        # 标签清空
        article_query.first().tag.clear()
        # 添加标签
        add_article_tags(tags,article_query.first())
        
        res['data'] = article_query.first().nid
        return JsonResponse(res)

class ArticleDiggView(View):
    def post(self, request, nid):
        res = {
            'code': 412,
            'msg': '点赞成功',
            'data': 0,
        }

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(digg_count=F('digg_count') + 1)
        # 查询查询数量
        digg_count = article_query.first().digg_count
        res['data'] = digg_count
        res['code'] = 0
        return JsonResponse(res)

class ArticleCollectView(View):
    def post(self, request, nid):
        # 同样的请求，收藏变取消收藏
        res = {
            'code': 412,
            'msg': '文章收藏成功！',
            'data': 0,
            'isCollect':True,
        }
        # 判断登录
        if not request.user.username:
            res['msg'] = '您还未登录，无法收藏！'
            return JsonResponse(res)
        # 判断用户是否收藏过-多对多关系Articles和UserInfo
        flag = request.user.collects.filter(nid=nid)
        num = 1
        if flag:
            # 用户已经收藏过了，取消收藏
            res['msg'] = '文章取消收藏成功！'
            request.user.collects.remove(nid)
            res['isCollect'] = True
            num = -1
        else:
            request.user.collects.add(nid)
            res['isCollect'] = False
        Articles.objects.filter(nid=nid).update(collects_count=F('collects_count') + num)
        res['data'] = Articles.objects.filter(nid=nid).first().collects_count
        res['code'] = 0

        # 一个用户只能收藏一次
        return JsonResponse(res)

