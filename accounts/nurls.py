from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts.admin import normaladminsite
from frontend.views import search

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nktc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(normaladminsite.urls)),
    url(r'^ueditor/',include('Ueditor.urls')),
    url(r'^search/$', search, name="search"),
)
