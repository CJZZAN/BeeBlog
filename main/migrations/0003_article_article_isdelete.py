# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-23 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191123_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='article_isdelete',
            field=models.IntegerField(default=0),
        ),
    ]
