# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('keyword', models.CharField(unique=True, max_length=50, verbose_name='\u5173\u952e\u5b57')),
                ('title', models.CharField(max_length=20, verbose_name='\u6807\u9898')),
                ('text', models.CharField(max_length=50, verbose_name='\u63cf\u8ff0\u6587\u5b57')),
                ('img', models.ImageField(upload_to=b'', verbose_name='\u5c01\u9762\u56fe\u7247')),
                ('url', models.URLField(verbose_name='\u539f\u6587\u94fe\u63a5')),
            ],
            options={
                'verbose_name': '\u56de\u590d\u56fe\u6587\u6d88\u606f',
                'verbose_name_plural': '\u56de\u590d\u56fe\u6587\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('keyword', models.CharField(unique=True, max_length=50, verbose_name='\u5173\u952e\u5b57')),
                ('reply', models.CharField(max_length=200, verbose_name='\u56de\u590d\u5185\u5bb9')),
            ],
            options={
                'verbose_name': '\u56de\u590d\u6587\u672c\u6d88\u606f',
                'verbose_name_plural': '\u56de\u590d\u6587\u672c\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='WechatDialogue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=255, verbose_name='\u5185\u5bb9')),
                ('replied', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u6d88\u606f',
                'verbose_name_plural': '\u6d88\u606f',
            },
        ),
        migrations.CreateModel(
            name='WechatUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('source', models.CharField(max_length=255, verbose_name='\u6765\u6e90\u7528\u6237OpenID')),
                ('target', models.CharField(max_length=255, verbose_name='\u76ee\u6807\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u4fe1\u606f',
            },
        ),
        migrations.AddField(
            model_name='wechatdialogue',
            name='user',
            field=models.ForeignKey(verbose_name='\u7528\u6237\u4fe1\u606f', to='wechat.WechatUser'),
        ),
    ]
