from django import template

register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name,article=None):
    img_list = [
        '/static/my/img/banner/banner1.jpg',
        '/static/my/img/banner/banner2.jpg',
    ]
    if article:
        #说明是文章详情页面
        #拿到文章封面
        cover = article.cover.url.url
        img_list = [cover]
        pass
    return {'img_list': img_list}
