"""fblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

from fblog import settings
from web import views as web_views
from web import upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'favicon.ico', RedirectView.as_view(url=settings.STATIC_URL+r'media/icon/favicon.ico')),
    path('', web_views.IndexView.as_view(), name='index'),
    path('search/', web_views.SearchView, name='search'),
    path('login/', web_views.OAuthLoginView.as_view(), name='login'),
    #github回调url
    path('github/oauth/', web_views.GitHubOAuthView.as_view(), name='github_oauth'),
    #要在url中提供next参数，注销后转向next中的url
    path('logout/', LogoutView.as_view(), name='logout'),
    path('article/<int:pk>', web_views.ArticleView.as_view(), name='article'),
    path('article/<int:pk>/comment/', web_views.CommentView.as_view(), name='article_comment'),
    path('article/<int:pk>/reply/', web_views.CommentReplyView.as_view(), name='article_reply'),
    path('category/<str:cate>/', web_views.CategoryView.as_view(), name='category'),
    path('archive/<str:date>/', web_views.ArchiveView.as_view(), name='archive'),
    re_path(r'^upload/image/$', upload.uploadImage, name='upload_image'),
]
