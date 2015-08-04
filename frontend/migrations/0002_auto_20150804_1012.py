# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import Ueditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': '\u9996\u9875\u70ed\u70b9\u63a8\u9001', 'verbose_name_plural': '\u9996\u9875\u70ed\u70b9\u63a8\u9001'},
        ),
        migrations.AlterModelOptions(
            name='slider',
            options={'verbose_name': '\u5e7b\u706f\u7247\u63a8\u9001', 'verbose_name_plural': '\u5e7b\u706f\u7247\u63a8\u9001'},
        ),
        migrations.AddField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4'),
        ),
        migrations.AddField(
            model_name='article',
            name='modify_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u4fee\u6539\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 1360px*260px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Activity', verbose_name='\u6709\u6548\u6d3b\u52a8\u5c01\u9762'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='old_img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 250px*90px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Activity', verbose_name='\u8fc7\u671f\u6d3b\u52a8\u5c01\u9762'),
        ),
        migrations.AlterField(
            model_name='article',
            name='cover_img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 600px*325px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Article', verbose_name='\u5c01\u9762\u56fe\u7247'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=Ueditor.models.UEditorField(verbose_name='\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='mainmenu',
            name='order',
            field=models.IntegerField(verbose_name='\u663e\u793a\u987a\u5e8f', blank=True),
        ),
        migrations.AlterField(
            model_name='secondarymenu',
            name='img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 600px*200px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Menu', verbose_name='\u5c55\u793a\u56fe\u7247'),
        ),
        migrations.AlterField(
            model_name='slider',
            name='img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: 300px*200px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', upload_to='img/Slider', verbose_name='\u5c55\u793a\u56fe\u7247'),
        ),
    ]
