# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from werobot import WeRoBot
from werobot.reply import TextReply, ArticlesReply, Article

from wechat.models import Message, Articles, WechatDialogue, WechatUser
from vote.models import VoteUser, Vote, Question


robot = WeRoBot(token='a16sJvhernrFeUZSrnKNKzIJMqt4G')


@robot.subscribe
def subscribe(message):
    return """
        欢迎关注创新人才。 mo-可爱

        这里
        会有高端的科技介绍，会有唯美的文艺散文
        会有精彩的社团展示，会有高雅的艺术展演

        敬请关注我们~如果你有好的建议，请发给我们哦~
        """

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


@robot.filter("投票")
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
    try:
        r = Message.objects.get(keyword=content)
        send = TextReply(message=message, content=r.reply)
        return send
    except:
        pass

@robot.text
def reply_article(message):
    content = message.content.strip()
    try:
        r = Articles.objects.get(keyword=content)
        send = ArticlesReply(message=message)
        article = Article(
            title=r.title,
            description=r.text,
            img='/media/' + r.img.url,
            url=r.url
        )
        send.add_article(article)
        return send
    except:
        pass

@robot.text
def dialogue(message):
    content = message.content.strip()
    wechat_user = WechatUser(source=message.source,target=message.target)
    wechat_user.save()
    wechat_dialogue = WechatDialogue(content=content, user=wechat_user)
    wechat_dialogue.save()  # TODO: 发送邮件给运营人员，提醒回复
    send = TextReply(message=message, content="消息已经收到啦~我们会尽快回复你哒~")
    return send