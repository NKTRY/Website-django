# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include
from frontend.views import index, main_menu, secondary_menu, secondary_menu_all, search, content

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^s/(?P<main>\w+)/$', main_menu, name="main_menu"),
    url(r'^s/(?P<main>\w+)/(?P<secondary>\w+)/$', secondary_menu, name="secondary_menu"),
    url(r'^a/(?P<main>\w+)/(?P<secondary>\w+)/$', secondary_menu_all, name="secondary_menu_all"),
    url(r'^search/$', search, name="search"),
    url(r'^s/(?P<main>\w+)/(?P<secondary>\w+)/(?P<id>\d+)/$', content, name="content"),
    url(r'^ueditor/',include('DjangoUeditor.urls'))
)