# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-14 04:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='installed_apps',
            field=models.TextField(default='msg,gmail,setit,calc,conts,apstr'),
        ),
    ]
