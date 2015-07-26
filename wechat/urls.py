from django.conf.urls import patterns, include, url
from django_werobot import make_view
from wechat.views import werobot_view

urlpatterns = patterns('',
    url(r'^$', werobot_view, name='werobot_view'),
)