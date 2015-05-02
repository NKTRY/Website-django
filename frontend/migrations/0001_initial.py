# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name='\u6807\u9898')),
                ('text', models.TextField(max_length=254, verbose_name='\u6d3b\u52a8\u7b80\u4ecb')),
                ('img', models.ImageField(upload_to='img/Activity', verbose_name='\u6d3b\u52a8\u5ba3\u4f20\u56fe\u7247')),
                ('url', models.URLField(verbose_name='\u6d3b\u52a8\u94fe\u63a5')),
                ('pub_date', models.DateField(verbose_name='\u53d1\u5e03\u65e5\u671f')),
                ('end_date', models.DateField(verbose_name='\u6d3b\u52a8\u7ed3\u675f\u65e5\u671f')),
                ('author', models.ForeignKey(verbose_name='\u53d1\u5e03\u4eba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6d3b\u52a8',
                'verbose_name_plural': '\u6d3b\u52a8',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=20, verbose_name='\u6807\u9898')),
                ('text', DjangoUeditor.models.UEditorField(verbose_name='\u5185\u5bb9')),
                ('pub_date', models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4', blank=True)),
                ('available', models.BooleanField(default=True, verbose_name='\u5df2\u53d1\u8868')),
                ('hits', models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u91cf')),
                ('category', models.CharField(max_length=20, verbose_name='\u5185\u5bb9\u5206\u7c7b', choices=[('dt', '\u793e\u56e2\u52a8\u6001'), ('zl', '\u793e\u56e2\u8d44\u6599')])),
                ('author', models.ForeignKey(verbose_name='\u4f5c\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u677f\u5757\u540d\u79f0')),
                ('codename', models.CharField(unique=True, max_length=20, verbose_name='\u673a\u8bfb\u540d\u79f0')),
                ('order', models.IntegerField(verbose_name='\u663e\u793a\u987a\u5e8f', blank=True)),
                ('img', models.ImageField(upload_to='img/Menu', verbose_name='\u5c55\u793a\u56fe\u7247')),
                ('available', models.BooleanField(default=True, verbose_name='\u5df2\u53d1\u5e03')),
            ],
            options={
                'verbose_name': '\u4e3b\u83dc\u5355',
                'verbose_name_plural': '\u4e3b\u83dc\u5355',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('url', models.URLField(verbose_name='\u6587\u7ae0\u94fe\u63a5', blank=True)),
                ('category', models.CharField(default='', max_length=20, verbose_name='\u5206\u7c7b', choices=[('nktc', 'NKTC'), ('nksu', '\u5b66\u751f\u4f1a'), ('shetuan', '\u793e\u56e2\u6d3b\u52a8')])),
                ('push', models.OneToOneField(verbose_name='\u63a8\u9001\u6587\u7ae0\u6807\u9898', to='frontend.Article')),
            ],
            options={
                'verbose_name': '\u9996\u9875\u63a8\u9001',
                'verbose_name_plural': '\u9996\u9875\u63a8\u9001',
            },
        ),
        migrations.CreateModel(
            name='SecondaryMenu',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=20, verbose_name='\u677f\u5757\u540d\u79f0')),
                ('codename', models.CharField(unique=True, max_length=20, verbose_name='\u673a\u8bfb\u540d\u79f0')),
                ('order', models.IntegerField(verbose_name='\u663e\u793a\u987a\u5e8f', blank=True)),
                ('img', models.ImageField(upload_to='img/Menu', verbose_name='\u5c55\u793a\u56fe\u7247')),
                ('available', models.BooleanField(default=True, verbose_name='\u5df2\u53d1\u5e03')),
                ('parent', models.ForeignKey(verbose_name='\u7236\u7ea7\u83dc\u5355', to='frontend.MainMenu')),
            ],
            options={
                'verbose_name': '\u6b21\u7ea7\u83dc\u5355',
                'verbose_name_plural': '\u6b21\u7ea7\u83dc\u5355',
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=20, verbose_name='\u63a8\u9001\u7b80\u4ecb')),
                ('img', models.ImageField(upload_to='img/Slider', verbose_name='\u5c55\u793a\u56fe\u7247')),
                ('url', models.URLField(verbose_name='\u6587\u7ae0\u94fe\u63a5', blank=True)),
                ('category', models.ForeignKey(verbose_name='\u5206\u7c7b', to='frontend.SecondaryMenu')),
                ('push', models.OneToOneField(verbose_name='\u63a8\u9001\u6587\u7ae0\u6807\u9898', to='frontend.Article')),
            ],
            options={
                'verbose_name': '\u9996\u9875\u5e7b\u706f\u7247',
                'verbose_name_plural': '\u9996\u9875\u5e7b\u706f\u7247',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='parent',
            field=models.ForeignKey(verbose_name='\u7236\u7ea7\u83dc\u5355', to='frontend.SecondaryMenu'),
        ),
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.ForeignKey(verbose_name='\u5206\u7c7b', to='frontend.SecondaryMenu'),
        ),
    ]
