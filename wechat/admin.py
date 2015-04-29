# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from accounts.admin import superadminsite

from wechat.models import Message, Articles
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ["keyword", "reply"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["keyword", "title"]


superadminsite.register(Message, MessageAdmin)
superadminsite.register(Articles, ArticleAdmin)