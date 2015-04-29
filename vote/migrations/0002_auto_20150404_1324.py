# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='choice',
            options={'verbose_name': '\u9009\u9879', 'verbose_name_plural': '\u9009\u9879'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u6295\u7968', 'verbose_name_plural': '\u6295\u7968'},
        ),
        migrations.AlterModelOptions(
            name='vote',
            options={'verbose_name': '\u9009\u7968', 'verbose_name_plural': '\u9009\u7968'},
        ),
        migrations.AlterField(
            model_name='choice',
            name='name',
            field=models.CharField(unique=True, max_length=20, verbose_name='\u9009\u9879\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u6295\u7968', to='vote.Question'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateField(verbose_name='\u7ed3\u675f\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='start_date',
            field=models.DateField(verbose_name='\u5f00\u59cb\u65f6\u95f4'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(unique=True, max_length=20, verbose_name='\u6295\u7968\u4ecb\u7ecd'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(unique=True, max_length=20, verbose_name='\u6295\u7968\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='choice',
            field=models.OneToOneField(verbose_name='\u6240\u5c5e\u9009\u9879', to='vote.Choice'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vote',
            name='user',
            field=models.CharField(max_length=200, verbose_name='\u6295\u7968\u4eba'),
            preserve_default=True,
        ),
    ]
