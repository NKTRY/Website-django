from django.shortcuts import render

# Create your views here.
from werobot.reply import create_reply
from werobot.parser import parse_user_msg
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from wechat.robot import robot


def werobot_view(request):
    f = open("/alidata/tmp.txt", "a")
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    signature = request.GET.get("signature", "")
    if not robot.check_signature(
        timestamp=timestamp,
        nonce=nonce,
        signature=signature
    ):
        print >> f, "Forbidden"
        return HttpResponseForbidden()
    if request.method == "GET":
        print >> f, "GET"
        return HttpResponse(request.GET["echostr"])
    elif request.method == "POST":
        body = request.body
        message = parse_user_msg(body)
        reply = robot.get_reply(message)
        print >> f, "POST: %s"%create_reply(reply, message=message)
        return HttpResponse(
            create_reply(reply, message=message),
            content_type="application/xml;charset=utf-8"
        )
    print >> f, "NotAllowed"
    f.close()
    return HttpResponseNotAllowed(['GET', 'POST'])