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
        (1, '前端'),
        (2, '后端'),
        (3, '项目相关')
    )
    category = models.IntegerField(verbose_name='文章分类', choices=category_choice, null=True, blank=True)
    tag = models.ManyToManyField(
        to='Tags',
        verbose_name='文章标签',
        blank=True
    )
    pwd = models.CharField(max_length=32,verbose_name='文章密码',null=True,blank=True)
    auther = models.CharField(max_length=16, verbose_name='作者', null=True, blank=True)
    source = models.CharField(max_length=32, verbose_name='来源', null=True, blank=True)

    link = models.URLField(verbose_name='文章链接',null=True,blank=True)

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
        to='UserInfo',
        to_field='nid',
        on_delete=models.CASCADE,
        verbose_name='评论者'
    )
    content = models.TextField(verbose_name='评论内容')
    comment_count = models.IntegerField(verbose_name='子评论数', default=0)
    drawing = models.TextField(verbose_name='配图', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='评论时间',auto_now_add=True)
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


# 新闻爬取记录
class New(models.Model):
    nid = models.AutoField(primary_key=True)
    # 注意auto_now_add是固定的 auto_now是变化的
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='获取时间')

    class Meta:
        verbose_name_plural = '新闻爬取'


# 文章封面
class Cover(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='文章封面地址', upload_to='article_img/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '文章封面'


@receiver(pre_delete, sender=Cover)  # sender你要删除或修改文件字段所在的类
def Cover_delete(instance, **kwargs):  # 函数名随意
    # print('进入文件删除方法，删除的是' ,instance.url)
    instance.url.delete(False)  # file是保存文件或图片的字段名


# 标签表
class Tags(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='标签名字')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章标签'


# 回忆录
class History(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='事件名称')
    content = models.TextField(verbose_name='事件内容')
    create_date = models.DateField(verbose_name='创建时间', null=True)
    drawing = models.TextField(verbose_name='配图组，以;隔开', null=True, blank=True)
    class Meta:
        verbose_name_plural = '回忆录'

#心情
class Moods(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, verbose_name='发布人')
    create_date = models.DateTimeField(verbose_name='发布时间',auto_now=True)
    content = models.TextField(verbose_name='心情内容')
    drawing = models.TextField(verbose_name='配图组，以;隔开', null=True, blank=True)
    comment_count = models.IntegerField(verbose_name='评论数',default=0)
    digg_count = models.IntegerField(verbose_name='评论数',default=0)
    avator = models.ForeignKey(
        to = 'Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='心情发布的头像'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '心情'

#心情评论
class MoodComment(models.Model):
    nid = models.AutoField(primary_key=True)
    avatar = models.ForeignKey(
        to = 'Avatars',
        to_field= 'nid',
        on_delete= models.SET_NULL,
        null = True,
        verbose_name='心情发布头像'
    )
    name = models.CharField(max_length=16,verbose_name='评论人',null=True)
    content = models.TextField(verbose_name='评论内容')
    digg_count = models.IntegerField(verbose_name='点赞数',default=0)
    mood = models.ForeignKey(
        to='Moods',
        to_field = 'nid',
        on_delete= models.SET_NULL,
        verbose_name='评论心情',
        null=True
    )
    create_date = models.DateTimeField(verbose_name='评论时间',auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '心情评论'

#网站导航
class Navs(models.Model):
    nid = models.AutoField(primary_key=True)
    nav_category = models.ForeignKey(
        to='NavCategory',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='网站导航分类',
        null = True
    )
    icon_href = models.URLField(verbose_name='图片链接',help_text='在线连接',null=True,blank=True)
    icon = models.FileField(verbose_name='网站图标',null=True,blank=True,
                            upload_to='site_icon/',help_text='文件优先级大于在线链接')
    title = models.CharField(max_length=32,verbose_name='网站标题')
    abstract = models.CharField(max_length=128,verbose_name='网站简介',null=True)
    create_date = models.DateTimeField(verbose_name='创建时间',auto_now=True)
    href = models.URLField(verbose_name='网站链接')
    status_choice = (
        (0,'待审核'),
        (1,'已通过'),
        (2,'被驳回')
    )
    status = models.IntegerField(verbose_name='导航状态',choices=status_choice,default=0)

    #定义一个函数
    def color_state(self):
        if self.status == 0:
            assign_state_name = '待审核'
            color_code = '#ec921e'
        elif self.status == 1:
            color_code = 'green'
            assign_state_name = '已通过'
        else:
            color_code = 'red'
            assign_state_name = '被驳回'
        return format_html(
            '<span style="color:{};">{}</span>'
        )
    color_state.short_description = '导航状态'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '网站导航'

#导航分类
class NavCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16,verbose_name='分类标题')
    icon = models.CharField(verbose_name='分类图标',max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '导航分类'

#站点背景
class Menu(models.Model):
    nid = models.AutoField(primary_key=True)
    menu_title = models.CharField(max_length=16, verbose_name='菜单名称')
    menu_title_en = models.CharField(max_length=32, verbose_name='菜单英文名字')
    title = models.CharField(max_length=32, verbose_name='slogen', null=True)
    abstract = models.TextField(verbose_name='slogen介绍', help_text='多个之间按分号区分', null=True)
    abstract_time = models.IntegerField(verbose_name='slogen切换时间', help_text='单位秒，默认8秒', default=8)
    rotation = models.BooleanField(verbose_name='是否轮播slogen介绍', default=True)
    menu_url = models.ManyToManyField(
        to='MenuImg',
        verbose_name='菜单图片',
        help_text='可以多选，多选就会轮播',
    )
    menu_rotation = models.BooleanField(verbose_name='是否轮播banner图', help_text='多选默认会轮播', default=False)
    menu_time = models.IntegerField(verbose_name='轮播图切换时间', default=8, help_text='单位秒,默认为8秒')

    class Meta:
        verbose_name_plural = '站点背景'


# 站点背景图
class MenuImg(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='图片地址', upload_to='site_bg/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '站点背景图'


# 广告表
class Advert(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, null=True)
    href = models.URLField(verbose_name='跳转链接')
    img = models.FileField(verbose_name='图片地址', null=True, blank=True, help_text='单图', upload_to='advert/')
    img_list = models.TextField(verbose_name='图片组', null=True, blank=True, help_text='上传图片请用线上地址，使用:隔开多张图片')
    is_show = models.IntegerField(verbose_name='是否展示', default=False)
    author = models.CharField(verbose_name='广告主', max_length=32, null=True, blank=True)
    abstract = models.CharField(verbose_name='产品介绍', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name_plural = '广告'


# 反馈信息
class Feedback(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(verbose_name='反馈信息')
    status = models.BooleanField(verbose_name='是否处理', default=False)
    processing_content = models.TextField(verbose_name='回复的内容', null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '用户反馈'
