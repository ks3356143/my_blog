from app01.models import Articles,Comment

def find_root_sub_comment(comment):
    if comment.parent_comment:
        return find_root_sub_comment(comment.parent_comment)
    return comment