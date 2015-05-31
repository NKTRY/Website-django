from django.conf.urls import patterns, include, url
from django_werobot import make_view
from wechat.robot import robot

urlpatterns = patterns('',
    url(r'^robot/', make_view(robot)),
)