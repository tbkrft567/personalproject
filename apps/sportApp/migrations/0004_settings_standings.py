# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-19 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportApp', '0003_team_image_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numOfTeams', models.IntegerField()),
                ('myTeam', models.CharField(max_length=45)),
                ('week_num', models.IntegerField()),
                ('season_num', models.IntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Standings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.IntegerField()),
                ('loses', models.IntegerField()),
                ('win_pct', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
