# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_auto_20150811_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='submit_to_baidu',
            field=models.BooleanField(default=False),
        ),
    ]
