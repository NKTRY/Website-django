from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from datetime import datetime

from vote.models import Vote, Question, Choice, VoteUser
from vote.forms import LoginForm
# Create your views here.


def index(request):
    question = Question.objects.filter(start_date__lte=datetime.today(), end_date__gte=datetime.today())
    context = {
        "questions": question,
    }
    return render(request, "vote/index.html", context=context)


def archive(request):
    question = Question.objects.filter(end_date__lte=datetime.today())
    context = {
        "question": question,
    }
    return render(request, "vote/archive.html", context=context)

def vote(request, question_id, wechat_id=None):
    if request.method == "GET":
        question = Question.objects.get(pk=question_id)
        choices = Choice.objects.filter(question=question)
        context = {
            "question": question,
            "choices": choices,
        }
        return render(request, "vote/vote-page.html", context=context)

    if request.method == "POST":
        if wechat_id != None:
            try:
                user = VoteUser.objects.get(openid=wechat_id)
                vote = Vote(choice=request.POST["choice"], user=user)
                vote.save()
                messages.success(request, "投票成功~")
            except:
                messages.warning(request, "请先发送“投票”到微信号《创新人才》获取相关信息")
        else:
            try:
                user = VoteUser.objects.get(username=request.session["vote_user"])
                vote = Vote(choice=request.POST["choice"], user=user)
                vote.save()
                messages.success(request, "投票成功~")
            except:
                messages.warning(request, "请先发送“投票”到微信号《创新人才》获取相关信息")
        return redirect('vote-page', {})


def login(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            if username != "" and password != "":
                try:
                    user = VoteUser.objects.get(username__exact = username,password__exact = password)
                    request.session["vote_user"] = user.username
                    return HttpResponse("You're logged in.")
                except:
                    return HttpResponse("Wrong password.")
    else:
        uf = loginForm()
    return render_to_response('login.html' , {'LoginForm':uf})


def logout(request):
     try:
         del request.session['member_id']
     except KeyError:
         pass
     return HttpResponse("You're logged out.")


def login(request):
     m = members.get_object(username__exact=request.POST['username'])
     if m.password == request.POST['password']:
         request.session['member_id'] = m.id
         return HttpResponse("You're logged in.")
     else:
         return HttpResponse("Your username and password didn't match.")