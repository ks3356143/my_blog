from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.db.models.signals import pre_delete  # 删除文件
from django.dispatch.dispatcher import receiver  # 删除文件


# 网站信息表
class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='网站标题')
    abstract = models.CharField(max_length=128, verbose_name='网站简介')
    key_words = models.CharField(max_length=128, verbose_name='网站关键字')
    record = models.CharField(max_length=32, verbose_name='网站备案号')
    create_date = models.DateTimeField(verbose_name='建站时间')
    version = models.CharField(max_length=16, verbose_name='网站版本号')
    icon = models.FileField(verbose_name='网站图标', upload_to='site_icon/')  # 注意存放位置

    def __str__(self):
        return self.title

    # 显示后台admin名字
    class Meta:
        verbose_name_plural = '网站信息'


# 个人信息
class MyInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='名字')
    job = models.CharField(max_length=128, verbose_name='工作')
    email = models.EmailField(max_length=64, verbose_name='邮箱')  # 新类型
    site_url = models.CharField(max_length=32, verbose_name='网站链接')
    addr = models.CharField(max_length=16, verbose_name='地址')
    bilibili_url = models.URLField(verbose_name='bilibili链接')
    guthub_url = models.URLField(verbose_name='GitHub地址')
    wechat_url = models.FileField(verbose_name='微信头像')  # 新类型
    qq_img = models.FileField(verbose_name='QQ图片', upload_to='my_info/')

    class Meta:
        verbose_name_plural = '个人信息'


# 用户表
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    sign_choice = (
        (0, '用户注册'),
        (1, '手机号注册'),
        (0, '邮箱注册'),
        (0, 'QQ注册'),
    )
    nick_name = models.CharField(max_length=16, verbose_name='昵称')
    sign_status = models.IntegerField(default=0, choices=sign_choice, verbose_name='注册方式')
    tel = models.CharField(max_length=12, verbose_name='手机号', null=True, blank=True)
    integral = models.IntegerField(default=20, verbose_name='用户积分')
    token = models.CharField(verbose_name='TOKEN', max_length=64, null=True, blank=True)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='用户头像',
        null=True
    )
    collects = models.ManyToManyField(
        to='Articles',
        verbose_name='收藏的文章'
    )

    class Meta:
        verbose_name_plural = '用户'


# 用户头像表
class Avatars(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='用户头像地址', upload_to='avatars/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '用户头像'


@receiver(pre_delete, sender=Avatars)  # sender = 你要删除或者修改文件字段的类
def download_delete(instance, **kwargs):
    instance.url.delete(False)  # file是保存文件或图片的字段名


# 文章表
class Articles(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32, null=True, blank=True)
    abstract = models.CharField(verbose_name='文章简介', max_length=128, null=True, blank=True)
    content = models.TextField(verbose_name='文章内容', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='文章创建日期', auto_now_add=True, null=True)  # 新属性
    change_date = models.DateTimeField(verbose_name='文章修改日期', auto_now=True, null=True)  # 这个日期会变
    status_choice = (
        (0, '未发布'),
        (1, '已发布'),
    )
    status = models.IntegerField(verbose_name='文章保存状态', choices=status_choice)
    recommend = models.BooleanField(verbose_name='是否上推荐', default='True')
    cover = models.ForeignKey(
        to='Cover',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='文章封面', null=True, blank=True
    )
    look_count = models.IntegerField(verbose_name='文章阅读量', default=0)
    comment_count = models.IntegerField(verbose_name='文章评论量', default=0)
    digg_count = models.IntegerField(verbose_name='文章点赞量', default=0)
    collects_count = models.IntegerField(verbose_name='文章收藏数', default=0)
    category_choice = (
        (0, '收藏'),
        (1, '后端')
    )
    category = models.IntegerField(verbose_name='文章分类', choices=category_choice, null=True, blank=True)
    tag = models.ManyToManyField(
        to='Tags',
        verbose_name='文章标签',
        blank=True
    )
    auther = models.CharField(max_length=16, verbose_name='作者', null=True, blank=True)
    source = models.CharField(max_length=32, verbose_name='来源', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'


# 评论表
class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    digg_count = models.IntegerField(verbose_name='点赞', default=0)
    article = models.ForeignKey(
        to='Articles',
        to_field='nid',
        on_delete=models.CASCADE,
        verbose_name='评论文章'
    )
    user = models.ForeignKey(
        to='Articles',
        to_field='nid',
        on_delete=models.CASCADE,
        verbose_name='评论者'
    )
    content = models.TextField(verbose_name='评论内容')
    comment_count = models.IntegerField(verbose_name='子评论数', default=0)
    drawing = models.TextField(verbose_name='配图', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='评论时间')
    parent_comment = models.ForeignKey(  # 新字段
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='是否为父评论'
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论'