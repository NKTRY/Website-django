# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(verbose_name="关键字", max_length=50, unique=True)
    reply = models.CharField(verbose_name="回复内容", max_length=200)

    class Meta:
        verbose_name = "回复文本消息"
        verbose_name_plural = "回复文本消息"

    def __unicode__(self):
        return self.keyword


class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(verbose_name="关键字", max_length=50, unique=True)
    title = models.CharField(verbose_name="标题", max_length=20)
    text = models.CharField(verbose_name="描述文字", max_length=50)
    img = models.ImageField(verbose_name="封面图片")
    url = models.URLField(verbose_name="原文链接")

    class Meta:
        verbose_name = "回复图文消息"
        verbose_name_plural = "回复图文消息"

    def __unicode__(self):
        return self.keyword


class WechatUser(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(verbose_name="来源用户OpenID", max_length=255)
    target = models.CharField(verbose_name="目标用户", max_length=255)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"


class WechatDialogue(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name="内容", max_length=255)
    user = models.ForeignKey(WechatUser, verbose_name="用户信息")
    replied = models.BooleanField(default=False)

    class Meta:
        verbose_name = "消息"
        verbose_name_plural = "消息"