from django.contrib import admin
from django.urls import path, re_path
# from django.views.static import serve
# from django.conf import settings
from api.views import login, article

# CBV模式
urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('sign/', login.SingView.as_view()),
    # 添加文章接口
    path('article/', article.ArticleView.as_view()),
]
