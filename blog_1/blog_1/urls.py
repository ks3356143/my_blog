
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path('',views.index),
]
