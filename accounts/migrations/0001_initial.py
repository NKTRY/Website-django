# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('changed_password', models.CharField(help_text='\u4fdd\u6301\u539f\u5bc6\u7801\u4e0d\u53d8\u8bf7\u7559\u7a7a', max_length=128, verbose_name='\u5bc6\u7801', blank=True)),
                ('nickname', models.CharField(max_length=10, verbose_name='\u6635\u79f0')),
                ('join_date', models.DateField(default=django.utils.timezone.now, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('last_login_date', models.DateField(default=django.utils.timezone.now, verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4')),
                ('is_nktc', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5141\u8bb8\u767b\u5f55NKTC\u7ba1\u7406\u5e73\u53f0')),
                ('locked', models.BooleanField(default=False, verbose_name='\u9501\u5b9a\u8d26\u6237')),
                ('expire', models.DateField(verbose_name='\u8d26\u6237\u6709\u6548\u671f')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
