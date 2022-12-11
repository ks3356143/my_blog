import os

if __name__ == "__main__":
    #加载Django项目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","blog_1.settings")
    import django

    django.setup()

    from app01.models import Articles,Comment
    comment_dict = {

    }
    # 方案一
    def find_root_comment(comment:Comment):
        # 找comment的最终根评论
        if comment.parent_comment:
            return find_root_comment(comment.parent_comment)
        return comment

    comment_query = Comment.objects.filter(article_id=1)

    for comment in comment_query:
        if not comment.parent_comment:
            comment_dict[comment.nid] = comment
            comment.sub_comment = [] #给每个父给个列表
            continue

    for comment in comment_query:
        for sub_comment in comment.comment_set.all():
            root_comment = find_root_comment(sub_comment)
            comment_dict[root_comment.nid].sub_comment.append(sub_comment)

    for k,v in comment_dict.items():
        print(v) #打印根评论
        for comment in v.sub_comment:
            print(comment) #打印子评论



