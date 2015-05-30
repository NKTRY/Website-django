# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from wechat.robot import robot
from django_werobot import make_view

urlpatterns = patterns('',
    url(r'^', make_view(robot)),
)