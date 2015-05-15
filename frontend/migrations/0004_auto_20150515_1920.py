# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0003_article_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='mainmenu',
            name='img',
        ),
        migrations.AddField(
            model_name='activity',
            name='old_img',
            field=models.ImageField(default='', upload_to='img/Activity', verbose_name='\u8fc7\u671f\u6d3b\u52a8\u5c01\u9762'),
        ),
        migrations.AddField(
            model_name='secondarymenu',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='\u677f\u5757\u4ecb\u7ecd'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='img',
            field=models.ImageField(upload_to='img/Activity', verbose_name='\u6709\u6548\u6d3b\u52a8\u5c01\u9762'),
        ),
    ]
