# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-11-26 19:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20191126_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='floor',
        ),
    ]
