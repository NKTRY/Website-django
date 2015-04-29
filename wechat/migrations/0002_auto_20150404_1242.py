# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='img',
            field=models.ImageField(upload_to=b'', verbose_name='\u5c01\u9762\u56fe\u7247'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articles',
            name='keyword',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u5173\u952e\u5b57'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articles',
            name='text',
            field=models.CharField(max_length=50, verbose_name='\u63cf\u8ff0\u6587\u5b57'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articles',
            name='title',
            field=models.CharField(max_length=20, verbose_name='\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articles',
            name='url',
            field=models.URLField(verbose_name='\u539f\u6587\u94fe\u63a5'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='keyword',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u5173\u952e\u5b57'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='reply',
            field=models.CharField(max_length=200, verbose_name='\u56de\u590d\u5185\u5bb9'),
            preserve_default=True,
        ),
    ]
