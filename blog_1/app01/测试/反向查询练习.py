import os

if __name__ == "__main__":
    #加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","blog_1.settings")
    import django

    django.setup()

    from app01.models import Articles,Comment
    comment_dict = {

    }
    # 一致comment-id查其关联的article
    comment_obj = Comment.objects.get(nid = 2)
    print(comment_obj)

    # 以下是报错的
    print(comment_obj.articles_set.all())



