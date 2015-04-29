# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from accounts.admin import superadminsite, normaladminsite

# 修改login页面url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nktc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(normaladminsite.urls)),
    url(r'^superadmin/', include(superadminsite.urls)),
    url(r'^', include('frontend.urls')),
    url(r'^werobot/', include('wechat.urls', namespace='werobot')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
)