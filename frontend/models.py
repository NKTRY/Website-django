# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from accounts.models import CustomUser

from DjangoUeditor.models import UEditorField
# Create your models here.


class MainMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="板块名称", max_length=20, unique=True)
    codename = models.CharField(verbose_name="机读名称", max_length=20, unique=True)
    order = models.IntegerField(verbose_name="显示顺序", blank=True)
    img = models.ImageField(verbose_name="展示图片", upload_to="img/Menu")
    available = models.BooleanField(verbose_name="已发布", default=True)

    class Meta:
        verbose_name = "主菜单"
        verbose_name_plural = "主菜单"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            content_type = ContentType.objects.get(app_label="frontend", model="Article")
        except:
            content_type = ContentType(app_label="frontend", model="Article", name="文章板块权限")
            content_type.save()

        translate = {"add": "添加", "delete": "删除", "change": "修改"}
        for permission in ["add", "delete", "change"]:
            try:
                codename = permission + "_" + self.codename + "_articles"
                Permission.objects.get(codename=codename)
            except:
                name = "允许" + translate[permission] + " " + self.name + " 内的文章"
                codename = permission + "_" + self.codename + "_articles"
                p = Permission(name=name, content_type=content_type, codename=codename)
                p.save()
        if self.order == None:
            self.order = self.id
        result = super(MainMenu, self).save()
        return result

    def delete(self, using=None):
        for permission in ["add", "delete", "change"]:
            codename = permission + "_" + self.codename + "_articles"
            p = Permission.objects.get(codename=codename)
            p.delete()
        result = super(MainMenu, self).delete()
        return result

    def __unicode__(self):
        return self.name


class SecondaryMenu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="板块名称", max_length=20, unique=True)
    codename = models.CharField(verbose_name="机读名称", max_length=20, unique=True)
    order = models.IntegerField(verbose_name="显示顺序", blank=True)
    img = models.ImageField(verbose_name="展示图片", upload_to="img/Menu")
    available = models.BooleanField(verbose_name="已发布", default=True)
    parent = models.ForeignKey(MainMenu, verbose_name="父级菜单")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            content_type1 = ContentType.objects.get(app_label="frontend", model="Article")
        except:
            content_type1 = ContentType(app_label="frontend", model="Article", name="文章板块权限")
            content_type1.save()

        try:
            content_type2 = ContentType.objects.get(app_label="frontend", model="Slider")
        except:
            content_type2 = ContentType(app_label="frontend", model="Slider", name="幻灯片推送权限")
            content_type2.save()

        try:
            content_type3 = ContentType.objects.get(app_label="frontend", model="Activity")
        except:
            content_type3 = ContentType(app_label="frontend", model="Activity", name="活动发布权限")
            content_type3.save()

        translate = {"add": "添加", "delete": "删除", "change": "修改"}
        for permission in ["add", "delete", "change"]:
            try:
                codename = permission + "_" + self.codename + "_articles"
                Permission.objects.get(codename=codename)
            except:
                name = "允许" + translate[permission] + " " + self.name + " 内的文章"
                codename = permission + "_" + self.codename + "_articles"
                p = Permission(name=name, content_type=content_type1, codename=codename)
                p.save()
            try:
                codename = permission + "_" + self.codename + "_sliders"
                Permission.objects.get(codename=codename)
            except:
                name = "允许" + translate[permission] + " " + self.name + " 内的幻灯片"
                codename = permission + "_" + self.codename + "_sliders"
                p = Permission(name=name, content_type=content_type2, codename=codename)
                p.save()
            try:
                codename = permission + "_" + self.codename + "_activities"
                Permission.objects.get(codename=codename)
            except:
                name = "允许" + translate[permission] + " " + self.name + " 内的活动"
                codename = permission + "_" + self.codename + "_activities"
                p = Permission(name=name, content_type=content_type3, codename=codename)
                p.save()
        if self.order == None:
            self.order = self.id
        result = super(SecondaryMenu, self).save()
        return result

    def delete(self, using=None):
        for permission in ["add", "delete", "change"]:
            codename = permission + "_" + self.codename + "_articles"
            p = Permission.objects.get(codename=codename)
            p.delete()
            codename = permission + "_" + self.codename + "_sliders"
            p = Permission.objects.get(codename=codename)
            p.delete()
            codename = permission + "_" + self.codename + "_activities"
            p = Permission.objects.get(codename=codename)
            p.delete()
        result = super(SecondaryMenu, self).delete()
        return result

    class Meta:
        verbose_name = "次级菜单"
        verbose_name_plural = "次级菜单"

    def __unicode__(self):
        return self.name


class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(verbose_name="推送简介", max_length=20)
    img = models.ImageField(verbose_name="展示图片", upload_to="img/Slider")
    url = models.URLField(verbose_name="文章链接", blank=True)
    push = models.OneToOneField("Article", verbose_name="推送文章标题")
    category = models.ForeignKey(SecondaryMenu, verbose_name="分类")

    class Meta:
        verbose_name = "首页幻灯片"
        verbose_name_plural = "首页幻灯片"

    def __unicode__(self):
        return self.text


class News(models.Model):
    category_choice = (
        ("nktc", "NKTC"),
        ("nksu", "学生会"),
        ("shetuan", "社团活动"),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="文章标题", max_length=20)
    url = models.URLField(verbose_name="文章链接", blank=True)
    push = models.OneToOneField("Article", verbose_name="推送文章标题")
    category = models.CharField(verbose_name="分类", max_length=20, default="", choices=category_choice)

    class Meta:
        verbose_name = "首页推送"
        verbose_name_plural = "首页推送"

    def __unicode__(self):
        return self.title


class Article(models.Model):
    category_choices = (
        ("dt", "社团动态"),
        ("zl", "社团资料"),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=20, unique=True)
    text = UEditorField('内容', width=600, height=300, toolbars="full".encode("raw_unicode_escape"), imagePath="img/Article",
                        filePath="file/Article", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None)
    author = models.ForeignKey(CustomUser, verbose_name="作者")
    pub_date = models.DateTimeField(verbose_name="发布时间", blank=True)
    available = models.BooleanField(verbose_name="已发表", default=True)
    hits = models.IntegerField(verbose_name="点击量", default=0)
    parent = models.ForeignKey(SecondaryMenu, verbose_name="父级菜单")
    category = models.CharField(verbose_name="内容分类", choices=category_choices, max_length=20)
    cover_img = models.ImageField(verbose_name="封面图片", upload_to="img/Article")
    description = models.TextField(verbose_name="简介", default="")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def hit(self):
        self.hits += 1
        self.save()

    def __unicode__(self):
        return self.title


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="标题", max_length=20)
    text = models.TextField(verbose_name="活动简介", max_length=254)
    img = models.ImageField(verbose_name="活动宣传图片", upload_to="img/Activity")
    url = models.URLField(verbose_name="活动链接")
    author = models.ForeignKey(CustomUser, verbose_name="发布人")
    pub_date = models.DateField(verbose_name="发布日期")
    category = models.ForeignKey(SecondaryMenu, verbose_name="分类")
    end_date = models.DateField(verbose_name="活动结束日期")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = "活动"

    def __unicode__(self):
        return self.title