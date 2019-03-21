from django.views.generic import  ListView, View
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.models import User

from datetime import datetime
import json, requests

from .models import Article, ArticleCategory, ArticleComment, ArticleCommentReply, Profile
from .models import ArticleCommentForm
from fblog import settings

# Create your views here.
class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p').order_by('-created_time')
        return article_list

class ArticleView(View):
    def get(self, request, *args, **kwargs):
        aid = self.kwargs.get('pk')
        article = get_object_or_404(Article, id=aid)
        article.increase_view()
        detail = Article.objects.filter(status='p', id=aid)
        comment_list = ArticleComment.objects.filter(article_id=aid, status='p').all()
        comment_num = ArticleComment.objects.filter(article_id=aid, status='p').all().count()
        reply_list = ArticleCommentReply.objects.filter(status='p').all()
        reply_num = ArticleCommentReply.objects.filter(comment__article_id=aid, status='p').count()
        form = ArticleCommentForm({'article': aid})
        comment_num += reply_num
        return render(request, 'article.html', {
            'article_list': detail,
            'form': form,
            'comment_list': comment_list,
            'comment_num': comment_num,
            'reply_list': reply_list,
        })

class CommentView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf8'))
        content = data.get('content')
        article_id = data.get('articleId')
        user_id = self.request.session['_auth_user_id']
        comment = ArticleComment.objects.create(
            content=content,
            article_id=article_id,
            user_id=user_id,
        )
        return HttpResponse(json.dumps({
            'content': comment.content,
            'articleId': comment.article_id,
            'user': str(comment.user),
            'time': str(comment.time),
            'num': comment.id
        }))

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf8'))
        commentId = data.get('commentId')
        ArticleComment.objects.filter(pk=commentId).delete()
        return HttpResponse(json.dumps({
            'success': True,
            'msg': '删除评论成功'
        }))

class CommentReplyView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf8'))
        commentId = data.get('commentId')
        replyContent = data.get('replyContent')
        replyCommentId = data.get('replyCommentId')
        reply = ArticleCommentReply.objects.create(
            content=replyContent,
            comment_id=commentId,
            reply_id=replyCommentId,
            user_id = self.request.session['_auth_user_id'],
        )
        return HttpResponse(json.dumps({
            'content': reply.content,
            'user': str(reply.user),
            'time': str(reply.time),
        }))

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf8'))
        replyId = data.get('replyId')
        ArticleCommentReply.objects.filter(pk=replyId).delete()
        return HttpResponse(json.dumps({
            'success': True,
            'msg': '删除回复成功'
        }))

class CategoryView(ListView):
    model = Article
    template_name = 'category.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        category = get_object_or_404(ArticleCategory, name=self.kwargs.get('cate'))
        return super(CategoryView, self).get_queryset().filter(category=category, status='p')

class ArchiveView(ListView):
    model = Article
    template_name = 'archive.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        date = datetime.strptime(self.kwargs.get('date'), '%Y-%m')
        article_list = Article.objects.filter(
            created_time__year=date.year,
            created_time__month=date.month,
            status='p'
        ).order_by('-created_time')
        return article_list

def SearchView(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'search.html', {'error_msg': error_msg})

    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    return render(request, 'search.html', {
        'error_msg': error_msg,
        'article_list': article_list,
        'q': q
    })

class OAuthLoginView(View):
    def get(self, request, *args, **kwargs):
        if 'next' in self.request.GET:
            # next为转到登录页面之前用户正在浏览的页面
            self.request.session['next'] = self.request.GET['next']
        github_oauth_url = 'https://github.com/login/oauth/authorize?client_id={}' \
        .format(settings.GITHUB_CLIENT_ID)
        return HttpResponse(github_oauth_url)

#基础OAuth视图
class OAuthView(View):
    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def get(self, request, *args, **kwargs):
        access_token = self.get_access_token(request)
        user_info = self.get_user_info(access_token)
        # 在子类中实现authenticate()方法
        return self.authenticate(user_info)

    def get_access_token(self, request):
        '获取access token'
        url = self.access_token_url
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            # code参数为GitHub转向至回调url时附带的
            'code': request.GET['code']
        }
        # 发送POST请求到access_token_url，带上client_id、client_secret、code这三个参数
        try:
            r = requests.post(url, data, headers=headers, timeout=60)
        except Exception as e:
            return HttpResponse('获取token失败:{}'.format(e))
        # 解析返回的json文本
        result = r.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            # 如果code过期了，则无法得到access_token
            raise PermissionDenied

    def get_user_info(self, access_token):
        '获取用户信息'
        url = self.user_api + access_token
        # 拿到access_token后调用api即可获得用户信息
        try:
            r = requests.get(url, timeout=60)
        except Exception as e:
            return HttpResponse('获取用户信息失败:{}'.format(e))
        # 用户信息也是json文本
        user_info = r.json()
        return user_info

    def get_success_url(self):
        '获取登录成功后返回的网页'
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            # 没有next就只能返回主页
            return '/index'

# GithubOAuth视图
class GitHubOAuthView(OAuthView):
    # 在具体类中定义相应的参数
    access_token_url = 'https://github.com/login/oauth/access_token'
    user_api = 'https://api.github.com/user?access_token='
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_SECRET_KEY

    def authenticate(self, user_info):
        '用户认证'
        user = User.objects.filter(profile__github_id=user_info['id'])
        # 在数据库中检索GitHub id
        # 如果有，则选择相应的用户登录
        # 如果没有，则创建用户，然后再登录
        if not user:
            user = User.objects.create_user(user_info['login'])
            profile = Profile(
                user=user,
                github_id=user_info['id'],
                avatar=user_info['avatar_url'])
            profile.save()
        else:
            user = user[0]
        # 用login函数登录，logout函数注销
        login(self.request, user)
        # 保存用户信息到session
        self.request.session['userName'] = user_info['login']
        self.request.session['userAvatar'] = user_info['avatar_url']
        self.request.session['userId'] = user_info['id']
        #print(self.request.session.keys())
        return redirect(self.get_success_url())