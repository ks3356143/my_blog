from django.contrib import admin
from django.urls import path, re_path, include
# from django.views.static import serve
# from django.conf import settings
from app01 import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('', views.index),
    path('news/', views.news),
    path('app01/utils/font/', views.get_code),
    path('logout/', views.logout),
    path('login/',views.login),
    path('sign/',views.sign),
    re_path(r'^article/(?P<nid>\d+)',views.article),

    re_path(r'^api/', include('api.urls')), #全部分发到api的app中
    #用户上传文件路由配置
    re_path(r'media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),

    #个人中心
    path('backend/',views.backend),
]
