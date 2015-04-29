# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werobot import WeRoBot
from werobot.utils import generate_token
from werobot.reply import TextReply, ArticlesReply, Article

from wechat.models import Message, Articles, WechatDialogue, WechatUser
from vote.models import VoteUser, Vote

import re

from vote.models import Question

robot = WeRoBot(token=generate_token(), enable_session=False)

@robot.subscribe
def subscribe(message):
    return 'Hello World!'


@robot.unsubscribe
def unsubscribe(message):
    try:
        user = VoteUser.objects.get(openid=message.source)
        vote = Vote.objects.filter(user=user)
        for obj in vote:
            obj.delete()
        user.delete()
    except:
        pass


@robot.filter(re.compile("投票"))
def reply_vote(message):
    votes = Question.objects.all()
    user = VoteUser(openid=message.source)
    user.save()
    if votes == []:
        return "现在没有进行中的投票哦~"
    else:
        link = ""
        for item in votes:
            pass  # TODO: 添加投票链接
        return link

@robot.text
def reply(message):
    content = message.content.strip()
    r = Message.objects.get(keyword=content)
    if r != []:
        send = TextReply(message=message, content=r.reply)
        return send

@robot.text
def reply_article(message):
    content = message.content.strip()
    r = Articles.objects.get(keyword=content)
    if r != []:
        send = ArticlesReply(message=message)
        article = Article(
            title=r.title,
            description=r.text,
            img=r.img,  # TODO: 替换为对应图片链接
            url=r.url
        )
        send.add_article(article)
        return send

@robot.text
def dialogue(message):
    content = message.content.strip()
    wechat_user = WechatUser(source=message.source,target=message.target)
    wechat_user.save()
    wechat_dialogue = WechatDialogue(content=content, user=wechat_user)
    wechat_dialogue.save()  # TODO: 发送邮件给运营人员，提醒回复
    send = TextReply(message=message, content="消息已经收到啦~我们会尽快回复你哒~")
    return send