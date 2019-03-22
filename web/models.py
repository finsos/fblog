from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput
from django.utils.html import strip_tags
import markdown
# Create your models here.

class Article(models.Model):
    STATUS = (
        ('d', '草稿'),
        ('p', '已发布')
    )

    title = models.CharField('标题', max_length=70)
    cover = models.ImageField(
        upload_to='cover',
        blank=True, null=True, verbose_name='封面图')
    content = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    abstract = models.CharField('摘要', max_length=100, blank=True, null=True,
                                help_text="可选，如若为空将摘取正文的前100个字符")
    status = models.CharField('文章状态', max_length=1, choices=STATUS)
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    toped = models.BooleanField('置顶', default=False)
    author = models.ForeignKey(User, verbose_name='作者', default='admin',
                               null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('ArticleCategory', verbose_name='分类',
                                 null=True, on_delete=models.SET_NULL)

    def increase_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.abstract:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.abstract = strip_tags(md.convert(self.content))[:100]
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def Meta(self):
        ordering = ['-last_modified_time']


class ArticleCategory(models.Model):
    name = models.CharField('类名', max_length=50)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    '用户资料'
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='account/avatar', max_length=200, null=True, blank=True, verbose_name='头像')
    github_id = models.PositiveIntegerField('GitHub id', unique=True, null=True, blank=True)

class BaseComment(models.Model):
    '基础评论模型'
    STATUS = (
        ('d', '待审核'),
        ('p', '已审核')
    )
    content = models.TextField('评论', max_length=500)
    time = models.DateTimeField('评论时间', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者')
    status = models.CharField('评论状态', max_length=1, default='d', choices=STATUS)

    class Meta:
        abstract = True

class ArticleComment(BaseComment):
    '文章评论'
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='评论文章')
    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.content

class ArticleCommentReply(BaseComment):
    '文章评论回复(二级评论)'
    comment = models.ForeignKey(ArticleComment, on_delete=models.CASCADE, related_name='replies', verbose_name='一级评论')
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='回复对象')
    class Meta:
        ordering = ['time']

class FriendLink(models.Model):
    name = models.CharField('友链名称', max_length=50)
    link = models.CharField('网址', max_length=50)
    valid = models.BooleanField('有效', max_length=1)

# Form Model
class ArticleCommentForm(ModelForm):
    class Meta:
        model = ArticleComment
        fields = [ 'content', 'article']
        widgets = {
            'article': HiddenInput,
        }

class ArticleCommentReplyForm(ModelForm):
    class Meta:
        model = ArticleCommentReply
        fields = ['content', 'comment', 'reply']
        widgets = {
            'comment': HiddenInput,
            'reply': HiddenInput,
        }