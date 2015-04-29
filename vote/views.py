from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import datetime

from vote.models import Vote, Question, Choice, VoteUser
# Create your views here.


def index(request):
    question = Question.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    context = {
        "questions": question,
    }
    return render(request, "vote/index.html", context=context)


def vote_page(request, question_id, wechat_id=None):
    if request.method == "GET":
        question = Question.objects.get(pk=question_id)
        choices = Choice.objects.filter(question=question)
        context = {
            "question": question,
            "choices": choices,
        }
        return render(request, "vote/vote-page.html", context=context)

    if request.method == "POST":
        try:
            user = VoteUser.objects.get(openid=wechat_id)
            vote = Vote(choice=request.POST["choice"], user=user)
            vote.save()
            messages.success(request, "投票成功~")
        except:
            messages.warning(request, "请先发送“投票”到微信号《创新人才》获取相关信息")