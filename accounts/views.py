from django.shortcuts import render

from accounts.models import CustomUser
# Create your views here.

def get_token(request, username):
    user = CustomUser.objects.filter(username=username)
    if user != []:
        # sendmail
        return "success"
    else:
        return "failed"