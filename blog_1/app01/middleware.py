from django.utils.deprecation import MiddlewareMixin
import json

#解析post请求的数据
class parse_json_post(MiddlewareMixin):
    #请求中间件
    def process_request(self,request):
        if request.method != "GET" and request.content_type=='application/json':
            print('进入了中间件！！')
            data = json.loads(request.body)
            request.data = data

    #响应中间件
    def process_response(self,request,response):
        return response