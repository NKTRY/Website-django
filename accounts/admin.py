# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry
from django.contrib.admin import AdminSite
from django.db.models import Q

from accounts.models import CustomUser
from accounts.forms import CustomAuthenticationForm, NormalAuthenticationForm

# Register your models here.


class NormalAdminSite(AdminSite):
    site_header = "NKTRY网站管理系统"
    site_title = "NKTRY网站管理系统"
    login_form = NormalAuthenticationForm
    login_template = "accounts/login.html"


class SuperAdminSite(AdminSite):
    site_header = "NKTRY网站管理系统"
    site_title = "NKTRY网站管理系统"
    login_form = CustomAuthenticationForm
    login_template = "admin/login.html"

    def has_permission(self, request):
        try:
            if not request.user.is_nktc:
                return False
            else:
                return request.user.is_active and request.user.is_staff
        except:
            return request.user.is_active and request.user.is_staff


class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {"fields": ("username", "changed_password", "nickname", "email", "expire")}),
        ("权限管理", {"fields": ("is_superuser", "user_permissions", "groups", "is_active", "is_staff",
                             "is_nktc", "locked")}),
    )

    list_display = ("username", "nickname", "email", "last_login_date")

    list_filter = ["is_active", "is_superuser", "is_nktc"]

    search_fields = ["username", "nickname", "email"]

    filter_horizontal = ["user_permissions", "groups"]

    def save_model(self, request, obj, form, change):
        if request.POST["changed_password"] != "":
            obj.password = make_password(request.POST["changed_password"])
            obj.changed_password = ""
        obj.save()


class NormalUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {"fields": ("username", "password", "nickname", "email", "expire")}),
        ("权限管理", {"fields": ("user_permissions", "locked")}),
    )

    list_display = ("username", "nickname", "email", "last_login_date")

    list_filter = ["is_active", "is_superuser", "is_nktc"]

    search_fields = ["username", "nickname", "email"]

    filter_horizontal = ["user_permissions"]

    def save_model(self, request, obj, form, change):
        if 'pbkdf2_sha256$' != request.POST["password"][:14]:
            obj.password = make_password(request.POST["password"])
        obj.is_staff = True
        obj.save()
        for i in request.user.groups.all():
            obj.groups.add(Group.objects.get(pk=i.id))
        obj.save()

    def get_queryset(self, request):
        qs = super(NormalUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        for item in request.user.groups.all():
            q = q | Q(groups__name__contains=item.name)
        return qs.filter(q)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "user_permissions":
                q = Q(id=-1)
                items = request.user.get_group_permissions()
                for item in items:
                    regex = re.compile(r".*\.(.*)")
                    perm = regex.findall(item)
                    q = q | Q(codename=perm[0])
                kwargs["queryset"] = Permission.objects.filter(q)
        return super(NormalUserAdmin, self).formfield_for_manytomany(db_field, request=None, **kwargs)


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ["permissions"]


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "__str__", "action_time"]

    readonly_fields = ["action_time", "user", "content_type", "object_id", "object_repr", "action_flag", "change_message"]

    search_fields = ["user__nickname", "action_time", "change_message", "content_type__model", "object_repr"]

    list_filter = ["action_time", "content_type"]


superadminsite = SuperAdminSite(name='superadmin')
superadminsite.disable_action("delete_selected")
superadminsite.register(CustomUser, CustomUserAdmin)
superadminsite.register(Permission)
superadminsite.register(Group, GroupAdmin)
superadminsite.register(LogEntry, LogEntryAdmin)

normaladminsite = NormalAdminSite(name='normaladmin')
normaladminsite.disable_action("delete_selected")
normaladminsite.register(CustomUser, NormalUserAdmin)
