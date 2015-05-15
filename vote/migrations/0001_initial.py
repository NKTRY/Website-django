# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u9009\u9879\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u9009\u9879',
                'verbose_name_plural': '\u9009\u9879',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=20, verbose_name='\u6295\u7968\u540d\u79f0')),
                ('text', models.CharField(unique=True, max_length=20, verbose_name='\u6295\u7968\u4ecb\u7ecd')),
                ('start_date', models.DateField(verbose_name='\u5f00\u59cb\u65f6\u95f4')),
                ('end_date', models.DateField(verbose_name='\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u6295\u7968',
                'verbose_name_plural': '\u6295\u7968',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('choice', models.OneToOneField(verbose_name='\u6240\u5c5e\u9009\u9879', to='vote.Choice')),
            ],
            options={
                'verbose_name': '\u9009\u7968',
                'verbose_name_plural': '\u9009\u7968',
            },
        ),
        migrations.CreateModel(
            name='VoteUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('openid', models.CharField(max_length=255, verbose_name='\u7528\u6237\u5fae\u4fe1ID')),
            ],
            options={
                'verbose_name': '\u6709\u6548\u7528\u6237',
                'verbose_name_plural': '\u6709\u6548\u7528\u6237',
            },
        ),
        migrations.AddField(
            model_name='vote',
            name='user',
            field=models.ForeignKey(verbose_name='\u6295\u7968\u7528\u6237', to='vote.VoteUser'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u6295\u7968', to='vote.Question'),
        ),
    ]
