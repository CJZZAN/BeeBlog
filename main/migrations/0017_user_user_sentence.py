# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-27 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_comment_floor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_sentence',
            field=models.CharField(default='博主很懒，什么都不写', max_length=200),
        ),
    ]
