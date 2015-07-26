from django.conf.urls import patterns, url
from django_werobot import make_view
from .robot import robot

urlpatterns = patterns('',
    url(r'^$', make_view(robot), name='werobot_view'),
)
