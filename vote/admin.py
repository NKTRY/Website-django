# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, requests

from django.contrib import admin
from django.db.models import Q

from accounts.admin import superadminsite, normaladminsite

from vote.models import Vote, Question, Choice, VoteUser
# Register your models here.


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["title", "question"]

    def get_queryset(self, request):
        qs = super(ChoiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1) | Q(question_author=request.user)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.img != None:
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


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline,]

    list_display = ["title", "start_date", "end_date"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "author":
                kwargs["queryset"] = CustomUser.objects.filter(username=request.user.username)
        return super(QuestionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1) | Q(author=request.user)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        origin_img = Image.open(obj.cover_img.path)
        watermark = Image.open("/alidata/www/Website-django/static/frontend/img/watermark.png")
        length = origin_img.size[0]/5
        width = length/2
        watermark = watermark.resize((length, width))
        if origin_img.mode != 'RGBA':
            origin_img = origin_img.convert('RGBA')
        layer = Image.new('RGBA', origin_img.size, (0, 0, 0, 0))
        layer.paste(watermark, (length*4, origin_img.size[1]-width))
        merge_img = Image.composite(layer, origin_img, layer)
        merge_img.save(obj.cover_img.path)


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp", "ip", "address", "choice", "user"]

    def save_model(self, request, obj, form, change):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip =  request.META['HTTP_X_FORWARDED_FOR']
        else:  
            ip = request.META['REMOTE_ADDR']
        obj.ip = ip
        try:
            url = "http://api.map.baidu.com/location/ip"
            querystring = {"ak":"UeB0D7k1XtZnmC9KTmHG5Eej", "ip":ip, "coor":"bd09ll"}
            response = requests.request("POST", url, params=querystring)
            rjson = json.loads(response.read())
            obj.address = rjson["address"]
        except:
            pass
        obj.save()


class VoteUserAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "openid", "is_active"]


superadminsite.register(Question, QuestionAdmin)
superadminsite.register(Choice, ChoiceAdmin)
superadminsite.register(Vote, VoteAdmin)
superadminsite.register(VoteUser, VoteUserAdmin)

normaladminsite.register(Question, QuestionAdmin)
normaladminsite.register(Choice, ChoiceAdmin)
normaladminsite.register(Vote, VoteAdmin)