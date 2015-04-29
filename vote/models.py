# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="投票名称", max_length=20, unique=True)
    text = models.CharField(verbose_name="投票介绍", max_length=20, unique=True)
    start_date = models.DateField(verbose_name="开始时间")
    end_date = models.DateField(verbose_name="结束时间")

    class Meta:
        verbose_name = "投票"
        verbose_name_plural = "投票"

    def __unicode__(self):
        return self.title


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="选项名称", max_length=20, unique=True)
    question = models.ForeignKey(Question, verbose_name="所属投票")

    class Meta:
        verbose_name = "选项"
        verbose_name_plural = "选项"

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    choice = models.OneToOneField(Choice, verbose_name="所属选项")
    user = models.ForeignKey("VoteUser", verbose_name="投票用户")

    class Meta:
        verbose_name = "选票"
        verbose_name_plural = "选票"

    def __unicode__(self):
        return self.choice


class VoteUser(models.Model):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(verbose_name="用户微信ID", max_length=255)

    class Meta:
        verbose_name = "有效用户"
        verbose_name_plural = "有效用户"

    def __unicode__(self):
        return self.openid