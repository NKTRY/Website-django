# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nickname', models.CharField(max_length=10, verbose_name='\u6635\u79f0')),
                ('join_date', models.DateField(default=datetime.datetime(2015, 3, 28, 14, 8, 18, 450000), verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_login_date', models.DateField(default=datetime.datetime(2015, 3, 28, 14, 8, 18, 450000), verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4')),
                ('use_token', models.BooleanField(default=False, verbose_name='\u4f7f\u7528\u52a8\u6001\u9a8c\u8bc1\u7801')),
                ('token', models.CharField(max_length=50, blank=True)),
                ('locked', models.BooleanField(default=False, verbose_name='\u9501\u5b9a\u8d26\u6237')),
                ('expire', models.DateField(verbose_name='\u8d26\u6237\u6709\u6548\u671f')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u7ba1\u7406',
                'verbose_name_plural': '\u7528\u6237\u7ba1\u7406',
                'permissions': (('can_view_customuser', '\u8bfb\u53d6\u7528\u6237\u8868'),),
            },
            bases=(models.Model,),
        ),
    ]
