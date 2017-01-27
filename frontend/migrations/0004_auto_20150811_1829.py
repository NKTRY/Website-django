# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_auto_20150809_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u6807\u9898'),
        ),
        migrations.RemoveField(
            model_name='secondarymenu',
            name='description',
        ),
    ]
