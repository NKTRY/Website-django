# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import AuthenticationForm
from django import forms

from django.contrib.auth import authenticate


class CustomAuthenticationForm(AuthenticationForm, forms.Form):
    token = forms.CharField(label="验证码", max_length=50, widget=forms.TextInput)

    error_messages = {
        'invalid_login': "请输入正确的用户名或密码，并确认验证码正确",
        'inactive': "账户未激活",
    }

    def confirm_login_allowed(self, user):
        if not user.check_status:
            raise forms.ValidationError(_("This account is inactive."), code='inactive')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        token = self.cleaned_data.get('token')

        if username and password and token:
            self.user_cache = authenticate(username=username, password=password, token=token)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class NormalAuthenticationForm(AuthenticationForm, forms.Form):
    error_messages = {
        'invalid_login': "请输入正确的用户名或密码",
        'inactive': "账户未激活",
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data