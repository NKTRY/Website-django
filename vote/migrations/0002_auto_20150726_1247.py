# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='name',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='text',
        ),
        migrations.AddField(
            model_name='choice',
            name='description',
            field=models.CharField(max_length=255, verbose_name='\u63cf\u8ff0', blank=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='img',
            field=models.ImageField(help_text='\u63a8\u8350\u5c3a\u5bf8: ---px*---px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c][\u53ef\u4ee5\u9009\u62e9\u4e0d\u6dfb\u52a0\u56fe\u7247]', upload_to='img/Vote', verbose_name='\u9009\u9879\u56fe\u7247', blank=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='url',
            field=models.URLField(verbose_name='\u8be6\u7ec6\u94fe\u63a5', blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(default='', verbose_name='\u6295\u7968\u53d1\u8d77\u4eba', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='cd_time',
            field=models.IntegerField(default=60, help_text='\u5982\u4e0d\u5141\u8bb8\u91cd\u590d\u6295\u7968\u6b64\u9879\u53ef\u586b\u4efb\u610f\u503c', verbose_name='\u6295\u7968\u7b49\u5f85\u65f6\u95f4[\u5355\u4f4d:s]'),
        ),
        migrations.AddField(
            model_name='question',
            name='cover_img',
            field=models.ImageField(default='', help_text='\u63a8\u8350\u5c3a\u5bf8: ---px*---px [\u5176\u4ed6\u5c3a\u5bf8\u8bf7\u4fdd\u6301\u957f\u5bbd\u6bd4\u76f8\u540c]', verbose_name='\u6295\u7968\u5c01\u9762\u56fe\u7247', upload_to='img/Vote'),
        ),
        migrations.AddField(
            model_name='question',
            name='description',
            field=models.CharField(default='', max_length=100, verbose_name='\u6295\u7968\u4ecb\u7ecd'),
        ),
        migrations.AddField(
            model_name='question',
            name='is_single_select',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u662f\u5355\u9879\u9009\u62e9'),
        ),
        migrations.AddField(
            model_name='question',
            name='max_choice',
            field=models.IntegerField(default=1, help_text='\u5982\u9009\u4e2d\u5355\u9879\u9009\u62e9\u6b64\u9879\u53ef\u586b\u4efb\u610f\u503c', verbose_name='\u6700\u591a\u9009\u9879\u6570'),
        ),
        migrations.AddField(
            model_name='question',
            name='max_vote',
            field=models.IntegerField(default=1, verbose_name='\u6700\u591a\u91cd\u590d\u6295\u7968\u6b21\u6570'),
        ),
        migrations.AddField(
            model_name='vote',
            name='address',
            field=models.CharField(default='', max_length=255, verbose_name='\u7269\u7406\u5730\u5740'),
        ),
        migrations.AddField(
            model_name='vote',
            name='ip',
            field=models.IPAddressField(default='0.0.0.0', verbose_name='IP\u5730\u5740'),
        ),
        migrations.AddField(
            model_name='vote',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u65f6\u95f4\u6233'),
        ),
        migrations.AddField(
            model_name='voteuser',
            name='changed_password',
            field=models.CharField(default='', max_length=20, verbose_name='\u4fee\u6539\u5bc6\u7801'),
        ),
        migrations.AddField(
            model_name='voteuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u8d26\u6237\u72b6\u6001'),
        ),
        migrations.AddField(
            model_name='voteuser',
            name='password',
            field=models.CharField(default='', max_length=50, verbose_name='\u5bc6\u7801'),
        ),
        migrations.AddField(
            model_name='voteuser',
            name='username',
            field=models.CharField(default='', unique=True, max_length=20, verbose_name='\u7528\u6237\u540d'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u9009\u9879', to='vote.Choice'),
        ),
    ]
