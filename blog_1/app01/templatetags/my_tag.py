from django import template
from app01.utils.search import Search
from django.utils.safestring import mark_safe
from app01.models import Tags
register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    img_list = [
        '/static/my/img/banner/banner1.jpg',
        '/static/my/img/banner/banner2.jpg',
    ]
    if article:
        # 说明是文章详情页面
        # 拿到文章封面
        cover = article.cover.url.url
        img_list = [cover]

        title = article.title
        abstract = article.abstract
        return {'img_list': img_list, 'title_banner': title, 'abstract_banner': abstract, 'article': article}
    return {'img_list': img_list}


@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('-change_date', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论'),
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')  # 如果没有就是空字符串
        order_list = [
            ([''], '全部字数'),
            (['0', '100'], '100字以内'),
            (['100', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内'),
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('','全部标签'))
        for tag in tag_list:
            order_list.append((tag.title,tag.title))

    query_params = request.GET.copy() #copy只取到一个word值

    order1 = Search(
        key=key,  # 接收一个key区分
        order=order,  # 参数：当前搜索状态
        order_list=order_list,
        query_params=query_params,  # 搜索条件，我要搜索python，如果有分页器东西移除
    )

    return mark_safe(order1.order_html())
