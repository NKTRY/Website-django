# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from datetime import datetime
# Create your models here.


class CustomUser(AbstractUser, models.Model):
    id = models.AutoField(primary_key=True)
    changed_password = models.CharField(verbose_name="密码", blank=True, help_text="保持原密码不变请留空", max_length=128)
    nickname = models.CharField(verbose_name="昵称", max_length=10)
    join_date = models.DateField(verbose_name="创建时间", default=timezone.now)
    last_login_date = models.DateField(verbose_name="上次登录时间", default=timezone.now)
    is_nktc = models.BooleanField(verbose_name="是否允许登录NKTC管理平台", default=False)
    locked = models.BooleanField(verbose_name="锁定账户", default=False)
    expire = models.DateField(verbose_name="账户有效期")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def check_status(self):
        today = datetime.date(timezone.now())
        if self.is_active and not self.locked and self.expire >= today:
            return True
        else:
            return False

    def update_login_date(self):
        self.last_login_date = timezone.now()
        self.save()

    def vaild_token(self, token):
        if self.token == token:
            return True
        else:
            return False