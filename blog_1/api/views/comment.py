from django.views import View
from django.http import JsonResponse
from app01.models import Comment,Articles
from django.db.models import F
# 以下是验证模块
from django import forms
from api.views.login import clean_form
# 以下是utils模块
from api.utils.utils import find_root_sub_comment
import json

class CommentView(View):
    # 发布评论
    def post(self,request):
        # 必填：文章id、用户、评论内容、回复人员（子评论）
        content = request.data['content']
        nid = request.data['nid']

        res = {
            'msg' : '文章评论成功！',
            'code' : 412,
            'self' :None
        }
        # 校验登录
        if not request.user.username:
            res['msg'] = '请先登录，才能发送评论'
            return JsonResponse(res)
        if not content:
            res['msg'] = "评论内容没有输入"
            res['self'] = 'content'
            return JsonResponse(res)
        cid = request.data.get("cid")
        #通过F查询找到comment_count然后加1
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count')+1)
        if cid:
            # 有cid的就不是根评论
            comment_object = Comment.objects.create(
                content=content,
                article_id=nid,
                user=request.user,
                parent_comment_id=cid
            )
            #根评论评论数加1
            root_comment_obj = find_root_sub_comment(comment_object)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
        else:
            #根评论
            Comment.objects.create(
                content=content,
                article_id=nid,
                user=request.user
            )
        res['code'] = 0
        return JsonResponse(res)

    # 删除评论
    def delete(self,request):
        # 自己发布的评论才能删除，或超级管理员，做验证，对象是不是user
        login_user = request.user
        res = {
            'code': 412,
            'msg': '评论删除成功！',
            'self': ''
        }

        data = request.data
        nid = data['nid']
        comment_user = Comment.objects.filter(nid=nid).first().user #当前用户
        if login_user == comment_user or login_user.is_superuser:
            # 先确认删除评论数量
            comment_obj = Comment.objects.filter(nid=nid).first()
            lenth = len(comment_obj.comment_set.all()) + 1
            root_comment_obj = find_root_sub_comment(comment_obj)
            root_comment_obj.comment_count -= lenth
            root_comment_obj.save()
            # 文章评论数减1
            comment_obj.article.comment_count -= lenth
            comment_obj.article.save()

            Comment.objects.filter(nid=nid).delete()
            res['code'] = 0
            return JsonResponse(res)
        # 如果不能删除
        res['msg'] = '你无法删除评论'

        return JsonResponse(res)

class CommentDiggView(View):
    def post(self,request,nid):
        res = {
            'code':412,
            'msg':'点赞成功',
            'data':0,
        }
        if not request.user.username:
            res['msg'] = '未登录无法点赞'
            return JsonResponse(res)

        comment_query = Comment.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)
        #查询查询数量
        digg_count = comment_query.first().digg_count
        res['data'] = digg_count
        res['code'] = 0
        return JsonResponse(res)
