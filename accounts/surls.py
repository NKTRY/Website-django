from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts.admin import superadminsite
from frontend.views import search

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nktc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include(superadminsite.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^ueditor/',include('Ueditor.urls')),
    url(r'^search/$', search, name="search"),
)
