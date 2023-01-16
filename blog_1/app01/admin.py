from django.contrib import admin
from app01.models import *
from django.utils.safestring import mark_safe


# Register your models here.后端注册表在后台显示
class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px;border-radius:5px">')
        return

    get_cover.short_description = '文章封面'

    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list

    get_tags.short_description = '标签'

    def get_title(self):
        return mark_safe(f"<a href='/article/{self.nid}' target='_blank'>{self.title}</a>")

    get_title.short_description = '文章地址'

    def get_edit_delete_btn(self):
        return mark_safe(f'''
            <a href="/backend/edit_article/{self.nid}" target="_blank">编辑</a>
            <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        ''')

    get_edit_delete_btn.short_description = '操作'

    list_display = [get_title, 'category', get_cover, get_tags,
                    'look_count', 'digg_count', 'comment_count', 'word',
                    'change_date', get_edit_delete_btn]

    # 字数统计动作
    def action_word(self, request, query_set):
        for obj in query_set:
            word = len(obj.content)
            obj.word = word
            print(obj, word)
            obj.save()

    action_word.short_description = '获取文章字数'
    action_word.type = 'success'
    actions = [action_word]


admin.site.register(Articles, ArticleAdmin)
admin.site.register(Cover)
admin.site.register(Tags)
admin.site.register(Comment)
admin.site.register(UserInfo)
admin.site.register(Avatars)
