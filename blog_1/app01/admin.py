from django.contrib import admin
from app01.models import Articles #文章表
from app01.models import Cover #文章封面表
from app01.models import Tags #文章标签表
from app01.models import Comment #文章标签表


# Register your models here.

admin.site.register(Articles)
admin.site.register(Cover)
admin.site.register(Tags)
admin.site.register(Comment)
