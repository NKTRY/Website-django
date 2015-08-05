# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from datetime import datetime

from vote.models import Vote, Question, Choice, VoteUser
from vote.forms import LoginForm
import vote.geetest as geetest
# Create your views here.


def index(request):
    question = Question.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    context = {
        "questions": question,
    }
    return render(request, "vote/index.html", context=context)


def archive(request):
    question = Question.objects.filter(end_date__lt=datetime.today())
    context = {
        "questions": question,
    }
    return render(request, "vote/archive.html", context=context)


@csrf_protect
def vote(request, question_id, wechat_id=None):
    if request.method == "GET":
        question = get_object_or_404(Question, pk=question_id)
        choices = Choice.objects.filter(question=question)
        gt = geetest.geetest(settings.CAPTCHA_ID, settings.PRIVATE_KEY)
        challenge = gt.geetest_register()
        BASE_URL = "api.geetest.com/get.php?gt="
        if len(challenge) == 32:
            geetest_url = "http://%s%s&challenge=%s" % (BASE_URL, settings.CAPTCHA_ID, settings.PRIVATE_KEY)
        context = {
            "question": question,
            "choices": choices,
            "geetest_url": geetest_url,
        }
        return render(request, "vote/vote-page.html", context=context)

    if request.method == "POST":
        challenge = request.POST.get('geetest_challenge', '')
        validate = request.POST.get('geetest_validate', '')
        seccode = request.POST.get('geetest_seccode', '')
        gt = geetest.geetest(settings.CAPTCHA_ID, settings.PRIVATE_KEY)
        result = gt.geetest_validate(challenge, validate, seccode)
        if not result:
            messages.warning(request, '验证失败')
            return redirect(reverse('vote-page', args=(question_id,)))
        if wechat_id == None:
            try:
                user = VoteUser.objects.get(username=request.session["vote_user"])
            except:
                messages.warning(request, '请先登录投票系统或发送"投票"到微信公众号"创新人才"获取投票链接')
                return redirect(reverse('vote-page', args=(question_id,)))
        else:
            try:
                user = VoteUser.objects.get(openid=wechat_id)
            except:
                messages.warning(request, '用户ID无效，请发送"投票"到微信公众号"创新人才"获取相关信息')
                return redirect(reverse('vote-page', args=(question_id,)))
        question = get_object_or_404(Question, pk=question_id)
        polls = request.POST.getlist("check_box_list")
        if len(polls) > question.max_choice:
            polls = polls[:question.max_choice]
        for poll in polls:
            poll_obj = get_object_or_404(Choice, id=int(poll))
            vote = Vote(choice=poll_obj, user=user)
            vote.save()
        messages.success(request, "投票成功~谢谢您的参与~")
        return redirect(reverse('vote_page', args=(question_id,)))


@csrf_protect
def login(request):
    if request.method == 'GET':
        return redirect('vote_index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username != "" and password != "":
            try:
                user = VoteUser.objects.get(username=username,password=password)
                request.session["vote_user"] = user.username
                messages.success(request, "登陆成功√")
            except:
                messages.warning(request, "请检查用户名和密码是否正确")
        else:
            messages.error(request, "请检查提交数据是否合法")
        return redirect('vote_index')


def logout(request):
    try:
        del request.session['vote_user']
    except KeyError:
        pass
    messages.success(request, "您已成功登出，感谢您今天登陆本站^_^")
    return redirect('vote_index')


@csrf_protect
def change_password(request):
    if request.method == 'GET':
        return redirect('vote_index')

    if request.method == 'POST':
        try:
            username = request.session["vote_user"]
        except:
            messages.warning(request, "请先登录本站-_-b")
            return redirect('vote_index')
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        if old_password != "" and new_password != "":
            try:
                user = VoteUser.objects.get(username=username, password=old_password)
                user.password = new_password
                user.save()
                del request.session["vote_user"]
            except:
                messages.warning(request, "请检查密码是否正确")
        else:
            messages.error(request, "请输入原密码和修改后密码>_<")
        return redirect('vote_index')


@csrf_protect
def register(request):
    if request.method == 'GET':
        return redirect('vote_index')

    if request.method == 'POST':
        username = request.POST["username"]
        passeord = request.POST["password"]
        openid = request.POST["token"]
        if username != "" and password != "" and openid != "":
            try:
                user = VoteUser.objects.get(openid=openid)
                if user.username == "" and user.password == "":
                    user.username = username
                    user.password = password
                    user.save()
                    messages.success(request, "恭喜您注册成功~")
                else:
                    messages.warning(request, "该认证码已经注册，请确认输入是否有误，如确认无误请联系网站管理员")
            except:
                messages.warning(request, "请确认认证码是否输入正确")
        else:
            messages.error(request, "请确定已填写全部内容再重新提交")
        return redirect('vote_index')