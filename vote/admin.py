# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, requests

from django.contrib import admin

from accounts.admin import superadminsite, normaladminsite

from vote.models import Vote, Question, Choice, VoteUser
# Register your models here.


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["name", "question"]

    def get_queryset(self, request):
        qs = super(ChoiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1) | Q(question_author=request.user)
        return qs.filter(q)


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
        return super(NormalArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(QuestionAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1) | Q(author=request.user)
        return qs.filter(q)


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