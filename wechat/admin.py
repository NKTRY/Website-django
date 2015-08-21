# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from PIL import Image

from accounts.admin import superadminsite
from wechat.models import Message, Articles
# Register your models here.


class MessageAdmin(admin.ModelAdmin):
    list_display = ["keyword", "reply"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["keyword", "title"]

    def save_model(self, request, obj, form, change):
        obj.save()
        origin_img = Image.open(obj.img.path)
        watermark = Image.open("/alidata/www/Website-django/static/frontend/img/watermark.png")
        length = origin_img.size[0]/5
        width = length/2
        watermark = watermark.resize((length, width))
        if origin_img.mode != 'RGBA':
            origin_img = origin_img.convert('RGBA')
        layer = Image.new('RGBA', origin_img.size, (0, 0, 0, 0))
        layer.paste(watermark, (length*4, origin_img.size[1]-width))
        merge_img = Image.composite(layer, origin_img, layer)
        merge_img.save(obj.img.path)


superadminsite.register(Message, MessageAdmin)
superadminsite.register(Articles, ArticleAdmin)