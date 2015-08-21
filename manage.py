# -*- coding:utf-8 -*-
#!/usr/bin/env python
import os
import sys


def createsu():
    username = raw_input("Please input username:\r\n")
    nickname = raw_input("Please input nickname:\r\n")
    password = raw_input("Please input password:\r\n")
    from accounts.models import CustomUser as C
    import datetime
    expire = datetime.datetime.now()+datetime.timedelta(days=2)
    u = C(username=username, nickname=nickname, is_nktc=True, expire=expire, is_staff=True, is_superuser=True)
    u.set_password(password)
    u.save()
    print u"请于24小时内登录后台修改账户有效期"



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nktc.settings")
    if sys.argv[1] == "createsu":
        createsu()
    else:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

