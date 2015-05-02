# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cover_img',
            field=models.ImageField(default='/', upload_to='img/Article', verbose_name='\u5c01\u9762\u56fe\u7247'),
            preserve_default=False,
        ),
    ]
