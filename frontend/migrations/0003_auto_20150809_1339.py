# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0002_auto_20150726_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondarymenu',
            name='img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 600px*370px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Menu', verbose_name='\u5c55\u793a\u56fe\u7247'),
        ),
    ]
