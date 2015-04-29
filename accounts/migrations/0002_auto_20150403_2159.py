# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='changed_password',
            field=models.CharField(help_text='\u4fdd\u6301\u539f\u5bc6\u7801\u4e0d\u53d8\u8bf7\u7559\u7a7a', max_length=128, verbose_name='\u5bc6\u7801', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='join_date',
            field=models.DateField(default=datetime.datetime(2015, 4, 3, 21, 59, 53, 176000), verbose_name='\u521b\u5efa\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_login_date',
            field=models.DateField(default=datetime.datetime(2015, 4, 3, 21, 59, 53, 176000), verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4'),
            preserve_default=True,
        ),
    ]
