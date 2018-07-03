# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-14 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_auto_20180614_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='installed_apps',
            field=models.TextField(default='messenger;/mainMessages,gmail;https://gmail.com,calculator;/calc,contacts;/contacts,appstore;/appstore'),
        ),
    ]