# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werobot import WeRoBot
from werobot.reply import TextReply, ArticlesReply, Article

from wechat.models import Message, Articles, WechatDialogue, WechatUser
from vote.models import VoteUser, Vote, Question


robot = WeRoBot(token='a16sJvhernrFeUZSrnKNKzIJMqt4G')


@robot.handler
def hello(message):
    return 'Hello World!'
