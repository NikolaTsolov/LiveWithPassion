# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-07 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20161226_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='times_visited',
            field=models.IntegerField(default=0),
        ),
    ]
