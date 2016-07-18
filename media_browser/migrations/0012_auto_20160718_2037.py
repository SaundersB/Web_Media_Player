# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-18 20:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_browser', '0011_auto_20160718_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiotrack',
            name='track_title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='audiotrack',
            name='date_added',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
