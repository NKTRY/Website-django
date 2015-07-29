# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.admin import superadminsite, normaladminsite

from vote.models import Vote, Question, Choice, VoteUser
# Register your models here.


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["name", "question"]


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline,]

    list_display = ["title", "start_date", "end_date"]


class VoteAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp", "ip", "address", "choice", "user"]


class VoteUserAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "openid", "is_active"]


superadminsite.register(Question, QuestionAdmin)
superadminsite.register(Choice, ChoiceAdmin)
superadminsite.register(Vote, VoteAdmin)
superadminsite.register(VoteUser, VoteUserAdmin)

normaladminsite.register(Question, QuestionAdmin)
normaladminsite.register(Choice, ChoiceAdmin)