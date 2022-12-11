from django.contrib import admin
from app01.models import Articles #文章表
from app01.models import Cover #文章封面表
from app01.models import Tags #文章标签表
from app01.models import Comment #文章标签表
from app01.models import UserInfo #用户表
from app01.models import Avatars #头像表，是个URL


# Register your models here.后端注册表在后台显示

admin.site.register(Articles)
admin.site.register(Cover)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(UserInfo)
admin.site.register(Avatars)
