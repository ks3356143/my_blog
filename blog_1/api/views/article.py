from django.http import HttpResponse,JsonResponse
from django.views import View

from markdown import markdown
from pyquery import PyQuery

class ArticleView(View):
    def post(self, request):
        res = {
            'msg':'文章发布成功',
            'code':412,
        }
        #发布文章-必须要标题和内容
        #文章简介如果为空，截取正文30个字符
        #其他可以不要，封面可以默认封面
        print(request.data)
        #校验title和content
        data:dict = request.data
        title = data["title"]
        content = data['content']
        if not title:
            res['msg'] = '请输入文章标题'
            return JsonResponse(res)
        if not content:
            res['msg'] = '请输入文章内容'
            return JsonResponse(res)
        #自己没有输入简介时候，解析markdown格式,解析html格式
        abstract = data['abstract']
        if not abstract:
            content_text = PyQuery(markdown(content)).text()
            data['abstract'] = content_text[0:30]

        return JsonResponse({'c':'c'})