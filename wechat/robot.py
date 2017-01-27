# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from werobot import WeRoBot
from werobot.reply import TextReply, ArticlesReply, Article
from django.core.urlresolvers import reverse
from django.conf import settings

from wechat.models import Message, Articles, WechatDialogue, WechatUser
from vote.models import VoteUser, Vote, Question


robot = WeRoBot(token=settings.WECHAT_TOKEN)


@robot.subscribe
def subscribe(message):
    return """
        欢迎关注南开中学体验创意中心微信公众平台——创新人才。 mo-可爱

        这里
        会有高端的科技介绍，会有唯美的文艺散文
        会有精彩的社团展示，会有高雅的艺术展演

        下面官菌来介绍一下获取电子表及社团简介的方法~~( ﹁ ﹁ ) ~~~
回复“00+社团编号”即可获得相应社团的电子纳新表~（如：输入“0001”即可get到体创的电子纳新表）(ง •̀_•́)ง
回复“js+社团编号”即可获得该社团的简介啦（如：输入“js01”即可获得体创的社团简介）！！
社团编号如下:
01南开中学体验创意中心协会
02 模拟联合国社团
03 红学社
04 南开Highlight英文社
05 体育协会
06 星尘天文社
07 溯源考古社 
08 OMG口语社
09 新视界生物社
10 青春海洋心理辅导社 
11 唇之声口哨社
12 话剧社  
13 国术社
14 爱心联盟
15 校报记者团                                        
16 落苏美食社
17 海棠书艺社
18 立体社                                            
19 辩论协会
20 JOY舞蹈社
21 数学社

     我们会继续更新社团电子纳新表哒~(๑•̀ㅂ•́)و✧
     敬请关注我们~如果你有好的建议，请发给我们哦~
        """

@robot.unsubscribe
def unsubscribe(message):
    try:
        user = VoteUser.objects.get(openid=message.source)
        user.is_active = False
        user.save()
    except:
        pass


@robot.filter("投票")
def reply_vote(message):
    votes = Question.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    try:
        user = VoteUser.objects.get(openid=message.source)
    except:
        user = VoteUser(openid=message.source)
        user.save()
    if len(votes) == 0:
        return "现在没有进行中的投票哦~您也可以发送'投票系统注册'获取投票系统注册码(=^.^=)登陆投票系统后可以直接进行投票哦[-.0]"
    else:
        link = ""
        for item in votes:
            url = reverse('vote_page_tmp', args=(item.id, message.source))
            link = link + '<a href="' + url + '">' + item.title + '</a><br>'
        link = link + "您也可以发送'投票系统注册'获取投票系统注册码(=^.^=)登陆投票系统后可以直接进行投票哦[-.0]"
        return link


@robot.filter("投票系统注册")
def reply_vote(message):
    return "您的注册码为：%s" % message.source


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
            img='http://www.nktry.com/media/' + r.img.url,
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
