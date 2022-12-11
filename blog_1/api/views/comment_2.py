from django.views import View #导入CBV模式
from django.http import JsonResponse #导入返回Json格式
from app01.models import Comment,Articles #导入数据库
from django.db.models import F

class Comment_2Views(View):
    #删除评论接口
    def post(self,request):
        res = {
            'code':412,
            'msg':'删除失败',
            'self':None,
        }
        nid = request.data.get("nid")
        # 验证是否为超级管理员或当前用户
        comment_user = Comment.objects.filter(nid=nid).first()
        login_user = request.user
        # 找到该根评论下所有子评论
        if login_user == comment_user or login_user.is_superuser:
            # 获取下面所有comment的数量
            comment_obj = Comment.objects.filter(nid=nid).first()
            lenth = len(comment_obj.comment_set.all())
            comment_obj.article.comment_count -= lenth + 1
            comment_obj.article.save()
            comment_obj.delete() #级联删除
            res['code'] = 0
            res['msg'] = '删除根评论成功'
        else:
            res['msg'] = '你没有权限删除该评论'

        return JsonResponse(res)