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
                ('keyword', models.CharField(unique=True, max_length=50)),
                ('title', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('img', models.URLField()),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('keyword', models.CharField(unique=True, max_length=50)),
                ('reply', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
