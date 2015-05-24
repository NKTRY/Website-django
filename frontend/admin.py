# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone

from accounts.admin import normaladminsite, superadminsite
from accounts.models import CustomUser

from frontend.models import Article, MainMenu, SecondaryMenu, Slider, Activity, News
# Register your models here.


class SuperArticleAdmin(admin.ModelAdmin):
    fieldsets = (
            ("文章内容", {"fields": ("title", "description", "text", "author")}),
            ("文章信息", {"fields": ("pub_date", "available", "parent", "cover_img")}),
        )

    list_display = ("title", "author", "pub_date", "hits", "parent", "available")

    list_filter = ["pub_date", "available", "parent"]

    search_fields = ["title", "author", "parent"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "author":
                kwargs["queryset"] = CustomUser.objects.filter(username=request.user.username)
            if db_field.name == "parent":
                q = Q(id=-1)
                main = MainMenu.objects.all()
                for item in main:
                    if request.user.has_perm("frontend.change_"+item.codename+"_articles"):
                        q = q | Q(parent=item)
                kwargs["queryset"] = SecondaryMenu.objects.filter(q)
        else:
            pass
        return super(SuperArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.pub_date == None:
            obj.pub_date = timezone.now()
        obj.save()


    def get_queryset(self, request):
        qs = super(SuperArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm1 = "frontend.change_"+item.codename+"_articles"
            perm2 = "frontend.change_"+item.parent.codename+"_articles"
            if request.user.has_perm(perm1) or request.user.has_perm(perm2):
                q = q | Q(parent=item)
        return qs.filter(q)


class NormalArticleAdmin(admin.ModelAdmin):
    fieldsets = (
            ("文章内容", {"fields": ("title", "description", "text", "author")}),
            ("文章信息", {"fields": ("parent", "cover_img", "available")}),
        )

    list_display = ("title", "author", "pub_date", "hits", "parent", "available")

    list_filter = ["pub_date", "available", "parent"]

    search_fields = ["title", "author", "parent"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "author":
                kwargs["queryset"] = CustomUser.objects.filter(username=request.user.username)
            if db_field.name == "parent":
                q = Q(id=-1)
                main = MainMenu.objects.all()
                for item in main:
                    if request.user.has_perm("frontend.change_"+item.codename+"_articles"):
                        q = q | Q(parent=item)
                kwargs["queryset"] = SecondaryMenu.objects.filter(q)
        return super(NormalArticleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(NormalArticleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm1 = "frontend.change_"+item.codename+"_articles"
            perm2 = "frontend.change_"+item.parent.codename+"_articles"
            if request.user.has_perm(perm1) or request.user.has_perm(perm2):
                q = q | Q(parent=item)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        if obj.pub_date == None:
            obj.pub_date = timezone.now()
        obj.save()


class SecondaryMenuInline(admin.TabularInline):
    model = SecondaryMenu
    extra = 1


class MainMenuAdmin(admin.ModelAdmin):
    fieldsets = (
                ("菜单信息", {"fields": ("name", "codename", "order", "available")}),
            )
    inlines = [SecondaryMenuInline]

    list_display = ["name", "codename", "order", "available"]

    list_filter = ["available"]

    search_fields = ["name", "codename"]

    def get_queryset(self, request):
        qs = super(MainMenuAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        main = MainMenu.objects.all()
        for item in main:
            if request.user.has_perm("frontend.change_"+item.codename+"_articles"):
                q = q | Q(codename=item.codename)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        model = MainMenu.objects.get(pk=obj.id)
        for permission in ["add", "delete", "change"]:
            try:
                codename = permission + "_" + model.codename + "_articles"
                permission = Permission.objects.get(codename=codename)
                permission.delete()
            except:
                pass
        obj.save()


class SecondaryMenuAdmin(admin.ModelAdmin):
    fieldsets = (
                ("菜单信息", {"fields": ("name", "codename", "img", "description", "order", "parent", "available")}),
            )
    list_display = ["name", "codename", "order", "available"]

    list_filter = ["available"]

    search_fields = ["name", "codename"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if request.user.is_superuser:
            pass
        else:
            if db_field.name == "parent":
                q = Q(id=-1)
                main = MainMenu.objects.all()
                for item in main:
                    if request.user.has_perm("frontend.add_"+item.codename+"_articles"):
                        q = q | Q(codename=item.codename)
                kwargs["queryset"] = MainMenu.objects.filter(q)
        return super(SecondaryMenuAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(SecondaryMenuAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        main = MainMenu.objects.all()
        for item in main:
            if request.user.has_perm("frontend.change_"+item.codename+"_articles"):
                q = q | Q(parent=item)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            if request.user.has_perm("frontend.change_"+item.codename+"_articles"):
                q = q | Q(codename=item.codename)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        model = MainMenu.objects.get(pk=obj.id)
        for permission in ["add", "delete", "change"]:
            try:
                codename = permission + "_" + model.codename + "_articles"
                permission = Permission.objects.get(codename=codename)
                permission.delete()
            except:
                pass
        obj.save()


class NormalSliderAdmin(admin.ModelAdmin):
    fieldsets = (("幻灯片内容", {"fields": ("text", "img", "url", "push", "category")}),)

    list_display = ["text", "push"]

    search_fields = ["text"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "push":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_sliders"):
                        q = q | Q(parent=item)
                kwargs["queryset"] = Article.objects.filter(q)
            if db_field.name == "category":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_sliders"):
                        q = q | Q(codename=item.codename)
                kwargs["queryset"] = SecondaryMenu.objects.filter(q)
        return super(NormalSliderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(NormalSliderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm = "frontend.change_"+item.codename+"_sliders"
            if request.user.has_perm(perm):
                q = q | Q(category=item)
        return qs.filter(q)


class SuperSliderAdmin(admin.ModelAdmin):
    fieldsets = (("幻灯片内容", {"fields": ("text", "img", "url", "push", "category")}),)

    list_display = ["text", "push"]

    search_fields = ["text"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "push":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_sliders"):
                        q = q | Q(parent=item)
                kwargs["queryset"] = Article.objects.filter(q)
            if db_field.name == "category":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_sliders"):
                        q = q | Q(category=item)
                kwargs["queryset"] = Slider.objects.filter(q)
        return super(SuperSliderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(SuperSliderAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm = "frontend.change_"+item.codename+"_sliders"
            if request.user.has_perm(perm):
                q = q | Q(category=item)
        return qs.filter(q)


class SuperActivityAdmin(admin.ModelAdmin):
    fieldsets = (("活动信息", {"fields": ("title", "text", "img", "old_img", "url", "category", "author", "pub_date", "end_date")}),)

    list_display = ["title", "url"]

    search_fields = ["title", "text"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_activities"):
                        q = q | Q(category=item)
                kwargs["queryset"] = Slider.objects.filter(q)
        return super(SuperActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(SuperActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm = "frontend.change_"+item.codename+"_activities"
            if request.user.has_perm(perm):
                q = q | Q(category=item)
        return qs.filter(q)


class NormalActivityAdmin(admin.ModelAdmin):
    fieldsets = (("活动信息", {"fields": ("title", "text", "img", "old_img", "url", "category", "author", "pub_date", "end_date")}),)

    list_display = ["title", "url"]

    search_fields = ["title", "text"]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "category":
                q = Q(id=-1)
                secondary = SecondaryMenu.objects.all()
                for item in secondary:
                    if request.user.has_perm("frontend.add_"+item.codename+"_activities"):
                        q = q | Q(codename=item.codename)
                kwargs["queryset"] = SecondaryMenu.objects.filter(q)
        return super(NormalActivityAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(NormalActivityAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        q = Q(id=-1)
        secondary = SecondaryMenu.objects.all()
        for item in secondary:
            perm = "frontend.change_"+item.codename+"_activities"
            if request.user.has_perm(perm):
                q = q | Q(category=item)
        return qs.filter(q)


class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "push"]

    search_fields = ["title"]


normaladminsite.register(Article, NormalArticleAdmin)
normaladminsite.register(MainMenu, MainMenuAdmin)
normaladminsite.register(SecondaryMenu, SecondaryMenuAdmin)
normaladminsite.register(Slider, NormalSliderAdmin)
normaladminsite.register(Activity, NormalActivityAdmin)

superadminsite.register(Article, SuperArticleAdmin)
superadminsite.register(MainMenu, MainMenuAdmin)
superadminsite.register(Slider, SuperSliderAdmin)
superadminsite.register(SecondaryMenu, SecondaryMenuAdmin)
superadminsite.register(Activity, SuperActivityAdmin)
superadminsite.register(News, NewsAdmin)