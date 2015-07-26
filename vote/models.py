# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="投票名称", max_length=20, unique=True)
    description = models.CharField(verbose_name="投票介绍", max_length=100)
    cd_time = models.IntegerField(verbose_name="投票等待时间[单位:s]", help_text="如不允许重复投票此项可填任意值")
    max_vote = models.IntegerField(verbose_name="最多重复投票次数")
    is_single_select = models.BooleanField(verbose_name="是否是单项选择")
    max_choice = models.IntegerField(verbose_name="最多选项数", help_text="如选中单项选择此项可填任意值")
    cover_img = models.ImageField(verbose_name="投票封面图片", upload_to="img/Vote", help_text="推荐尺寸: ---px*---px [其他尺寸请保持长宽比相同]")
    author = models.ForeignKey(CustomUser, verbose_name="投票发起人")
    start_date = models.DateField(verbose_name="开始时间")
    end_date = models.DateField(verbose_name="结束时间")

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = "投票"

    def __unicode__(self):
        return self.title


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="选项名称", max_length=20, unique=True)
    description = models.CharField(verbose_name="描述", max_length=255)
    url = models.URLField(verbose_name="详细链接", blank=True)
    img = models.ImageField(verbose_name="选项图片", upload_to="img/Vote", blank=True, help_text="推荐尺寸: ---px*---px [其他尺寸请保持长宽比相同][可以选择不添加图片]")
    question = models.ForeignKey(Question, verbose_name="所属投票")

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "选项"

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(verbose_name="时间戳", default=timezone.now)
    ip = models.IPAddressField(verbose_name="IP地址")
    address = models.CharField(verbose_name="物理地址", max_length=255)
    choice = models.ForeignKey(Choice, verbose_name="所属选项")
    user = models.ForeignKey("VoteUser", verbose_name="投票用户")

    class Meta:
        verbose_name = "选票"
        verbose_name_plural = "选票"

    def __unicode__(self):
        return self.choice


class VoteUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=20, unique=True)
    password = models.CharField(verbose_name="密码", max_length=50)
    changed_password = models.CharField(verbose_name="修改密码", max_length=20)
    is_active = models.BooleanField(verbose_name="账户状态", default=True)
    openid = models.CharField(verbose_name="用户微信ID", max_length=255)

    class Meta:
        verbose_name = "有效用户"
        verbose_name_plural = "有效用户"

    def __unicode__(self):
        return self.openid