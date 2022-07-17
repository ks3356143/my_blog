import os

if __name__ == "__main__":
    #加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","blog_1.settings")
    import django

    django.setup()

    from app01.models import Articles,Comment

    #找到某个文章的所有评论
    comment_dict = {

    }
    comment_query = Comment.objects.filter(article_id = 1)
    for comment in comment_query:
        if not comment.parent_comment: #找到父评论
            comment_dict[comment.nid] = comment #把根评论放入字典

        print(comment.comment_set)
