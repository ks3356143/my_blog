from app01.models import Articles,Comment

# 方案二
def find_root_sub_comment(root_comment:Comment,sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        # 找根评论的子评论-只能找到一个层级
        sub_comment_list.append(sub_comment)
        find_root_sub_comment(sub_comment,sub_comment_list)

def sub_comment_list(nid):
    comment_query = Comment.objects.filter(article_id=nid).order_by("-create_date")
    # 把评论储存到列表
    comment_list = []
    for comment in comment_query:
        if not comment.parent_comment:
            # 递归查找该根评论下面所有子评论
            lis = []
            find_root_sub_comment(comment,lis)
            comment.sub_comment = lis
            comment_list.append(comment)
            continue

    return comment_list