# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名：", max_length=20)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())