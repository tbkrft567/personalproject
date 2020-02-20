# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-21 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportApp', '0010_auto_20191121_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standings',
            name='pts_against_avg',
        ),
        migrations.RemoveField(
            model_name='standings',
            name='pts_for_avg',
        ),
        migrations.AddField(
            model_name='standings',
            name='pts_against',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='standings',
            name='pts_for',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]