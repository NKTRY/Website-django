# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone
from PIL import Image, ImageColor

from accounts.admin import normaladminsite, superadminsite
from accounts.models import CustomUser
from frontend.models import Article, MainMenu, SecondaryMenu, Slider, Activity, News
# Register your models here.


def check_size(length, width, filename):
    origin_img = Image.open(filename)
    watermark = Image.open("/alidata/www/Website-django/static/frontend/img/watermark.png")
    length_img = origin_img.size[0]
    width_img = origin_img.size[1]
    length_watermark = 100*length_img/length
    watermark = watermark.resize((length_watermark, length_watermark/2))
    if origin_img.mode != 'RGBA':
        origin_img = origin_img.convert('RGBA')
    if (length_img/width_img) > (length/width):
        W = length_img*width/length
        bg_img = Image.new(origin_img.mode, (length_img, W), ImageColor.getcolor('white', origin_img.mode))
        bg_img.paste(origin_img, (0, W/2-width_img/2))
        layer = Image.new('RGBA', (length_img, W), (0, 0, 0, 0))
        layer.paste(watermark, (length_img-length_watermark, W/2+width_img/2-length_watermark/2))
        bg_img = Image.composite(layer, bg_img, layer)
    if (length_img/width_img) < (length/width):
        L = width_img*length/width
        bg_img = Image.new(origin_img.mode, (L, width_img), ImageColor.getcolor('white', origin_img.mode))
        bg_img.paste(origin_img, (L/2-length_img/2, 0))
        layer = Image.new('RGBA', (L, width_img), (0, 0, 0, 0))
        layer.paste(watermark, (L/2+length_img/2-length_watermark, width_img-length_watermark/2))
        bg_img = Image.composite(layer, bg_img, layer)
    if (length_img/width_img) == (length/width):
        bg_img = origin_img
        layer = Image.new('RGBA', (length_img, width_img), (0, 0, 0, 0))
        layer.paste(watermark, (length_img-length_watermark, width_img-length_watermark/2))
        bg_img = Image.composite(layer, bg_img, layer)
    try:
        bg_img = bg_img.resize((length, width))
        bg_img.save(filename)
    except:
        pass


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
        check_size(600, 325, obj.cover_img.path)


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
        check_size(600, 325, obj.cover_img.path)


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
        try:
            model = MainMenu.objects.get(pk=obj.id)
            for permission in ["add", "delete", "change"]:
                try:
                    codename = permission + "_" + model.codename + "_articles"
                    permission = Permission.objects.get(codename=codename)
                    permission.delete()
                except:
                    pass
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
        try:
            model = MainMenu.objects.get(pk=obj.id)
            for permission in ["add", "delete", "change"]:
                try:
                    codename = permission + "_" + model.codename + "_articles"
                    permission = Permission.objects.get(codename=codename)
                    permission.delete()
                except:
                    pass
                try:
                    codename = permission + "_" + model.codename + "_sliders"
                    permission = Permission.objects.get(codename=codename)
                    permission.delete()
                except:
                    pass
                try:
                    codename = permission + "_" + model.codename + "_activities"
                    permission = Permission.objects.get(codename=codename)
                    permission.delete()
                except:
                    pass
        except:
            pass
        obj.save()
        check_size(600, 200, obj.img.path)

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
            perm_p = "frontend.change_"+item.parent.codename+"_sliders"
            if request.user.has_perm(perm) or request.user.has_perm(perm_p):
                q = q | Q(category=item)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        check_size(300, 200, obj.img.path)


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
            perm_p = "frontend.change_"+item.parent.codename+"_sliders"
            if request.user.has_perm(perm) or request.user.has_perm(perm_p):
                q = q | Q(category=item)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        check_size(300, 200, obj.img.path)


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
            perm_p = "frontend.change_"+item.parent.codename+"_activities"
            if request.user.has_perm(perm) or request.user.has_perm(perm_p):
                q = q | Q(category=item)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        check_size(1360, 260, obj.img.path)
        check_size(250, 90, obj.old_img.path)


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
            perm_p = "frontend.change_"+item.parent.codename+"_activities"
            if request.user.has_perm(perm) or request.user.has_perm(perm_p):
                q = q | Q(category=item)
        return qs.filter(q)

    def save_model(self, request, obj, form, change):
        obj.save()
        check_size(1360, 260, obj.img.path)
        check_size(250, 90, obj.old_img.path)



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