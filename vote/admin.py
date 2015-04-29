# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.admin import superadminsite

from vote.models import Vote, Question, Choice
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
    pass


superadminsite.register(Question, QuestionAdmin)
superadminsite.register(Choice, ChoiceAdmin)
superadminsite.register(Vote, VoteAdmin)