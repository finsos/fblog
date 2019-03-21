from django.contrib import admin
from web.models import Article, ArticleCategory, Profile, ArticleComment, ArticleCommentReply, FriendLink

# Register your models here.

#blog name
admin.site.site_header = "后台管理"

@admin.register(Article)
class AricleAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'created_time', 'last_modified_time', 'author', 'status')
    list_filter = ('created_time', 'status')
    list_editable = ('status', )

    class Media:
        css = {'all': (
            'css/simditor.css',
            'css/simditor-markdown.css',
            'css/simditor-emoji.css'
        )}
        js = (
            'js/jquery.min.js',
            'js/simditor/marked.js',
            'js/simditor/to-markdown.js',
            'js/simditor/module.js',
            'js/simditor/uploader.js',
            'js/simditor/hotkeys.js',
            'js/simditor/simditor.js',
            'js/simditor/simditor-autosave.js',
            'js/simditor/simditor-markdown.js',
            'js/simditor/simditor-emoji.js',
            'js/base.js',
            'js/simditor.js',
        )

@admin.register(ArticleCategory)
class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_time', 'last_modified_time')
    list_display_links = ('name', )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'github_id', 'avatar')
    list_filter = ('user', )

@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'content', 'article', 'time')
    list_filter = ('status', 'time', )
    list_editable = ('status',)
    actions = ['approve_comment']
    def approve_comment(self, request, queryset):
        rows_update = queryset.update(status='p')
        self.message_user(request, '{}条评论成功审批通过'.format(rows_update))

    approve_comment.short_description = '审批通过所选的评论'

@admin.register(ArticleCommentReply)
class ArticleCommentReplyAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'content', 'comment', 'reply', 'time')
    list_filter = ('status', 'time', )
    list_editable = ('status',)
    actions = ['approve_comment']
    def approve_comment(self, request, queryset):
        rows_update = queryset.update(status='p')
        self.message_user(request, '{}条回复成功审批通过'.format(rows_update))

    approve_comment.short_description = '审批通过所选的回复'

@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'valid')
    list_editable = ('link', )
