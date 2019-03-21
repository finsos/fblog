#!usr/bin/env python
# -*- coding: utf-8 -*-
# *******************************************************
# @File:     fblog_tags
# @Auth:     winver9@gmail.com
# @Create:   2019-3-6 10:43
# @License:  © Copyright 2019, LBlog Programs.
# *******************************************************
from django import template
from django.db.models.aggregates import Count
from ..models import ArticleCategory, Article, ArticleComment, FriendLink
from fblog import settings

register = template.Library()

@register.simple_tag
def get_all_categorys():
    #return Catagory.objects.all().order_by('-created_time')
    #return ArticleCategory.objects.annotate(num_article=Count('article')).filter(num_article__gt=0)
    return ArticleCategory.objects.filter(article__status='p').annotate(
        num_article=Count('article')).filter(num_article__gt=0)

@register.simple_tag
def get_archives():
    return Article.objects.dates('created_time', 'month', order='DESC')

@register.filter(name='month_article_num')
def month_article_num(value):
    return Article.objects.filter(created_time__month=value, status='p').count()

@register.simple_tag
def get_latest_article():
    return Article.objects.filter(status='p').order_by('-last_modified_time')[:10]

@register.simple_tag
def get_latest_comment():
    return ArticleComment.objects.filter(status='p').order_by('-time')[:10]

@register.simple_tag
def get_friendLikns():
    return FriendLink.objects.filter(valid=True)

@register.simple_tag
def get_blog_title():
    return list(settings.FBLOG_TITLE)

@register.filter(name='count_words')
def count_words(value):
    return len(value)

@register.filter(name='has_words')
def has_words(value, args):
    if args in value:
        return True
    return False

@register.filter(name='highlight')
def highlight(value, q):
    return value.replace(q, '<font color="red" size="5">{}</font>'.format(q))

if __name__ == '__main__':
    get_all_categorys()
    print(register.tags.keys())