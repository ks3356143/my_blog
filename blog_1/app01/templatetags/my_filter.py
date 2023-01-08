from django import template

register = template.Library()


@register.filter
def is_user_collects(article, request):  # 传入了一个article对象和request请求对象
    if str(request.user) == 'AnonymousUser':
        print(f'以{request.user}的方式查看文章')
        return None
    if article in request.user.collects.all():
        return 'show'

# 判断是否有文章内容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'
