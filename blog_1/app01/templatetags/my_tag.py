from django import template

register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    img_list = [
        'static/my/img/banner/banner1.jpg',
        'static/my/img/banner/banner2.jpg',
    ]
    print(menu_name)
    return {'img_list': img_list}
