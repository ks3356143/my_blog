from django.contrib import admin
from django.urls import path, re_path
from api.views import login, article, comment, comment_2

# CBV模式
urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('sign/', login.SingView.as_view()),
    # 添加文章接口
    path('article/', article.ArticleView.as_view()),
    # 编辑文章接口
    re_path('article/(?P<nid>\d+)', article.ArticleView.as_view()),
    # 发布评论接口
    re_path('article/comment/',comment.CommentView.as_view()),
    # 删除根评论接口
    re_path('article/rootcomment/',comment_2.Comment_2Views.as_view()),
    # 评论点赞
    re_path('comment/digg/(?P<nid>\d+)/',comment.CommentDiggView.as_view()),
    # 文章点赞
    re_path('article/digg/(?P<nid>\d+)/',article.ArticleDiggView.as_view()),
    # 文章收藏
    re_path('article/collect/(?P<nid>\d+)/',article.ArticleCollectView.as_view()),
]
