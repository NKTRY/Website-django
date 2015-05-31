from django.shortcuts import render

# Create your views here.
from werobot import WeRoBot
from werobot.parser import parse_user_msg
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed


robot = WeRoBot(token='a16sJvhernrFeUZSrnKNKzIJMqt4G')


@robot.handler
def hello(message):
    return 'Hello World!'


def werobot_view(request):
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    signature = request.GET.get("signature", "")
    if not robot.check_signature(
        timestamp=timestamp,
        nonce=nonce,
        signature=signature
    ):
        return HttpResponseForbidden()
    if request.method == "GET":
        return HttpResponse(request.GET["echostr"])
    elif request.method == "POST":
        body = request.body
        message = parse_user_msg(body)
        reply = robot.get_reply(message)
        return HttpResponse(
            reply,
            content_type="application/xml;charset=utf-8"
        )
    return HttpResponseNotAllowed(['GET', 'POST'])