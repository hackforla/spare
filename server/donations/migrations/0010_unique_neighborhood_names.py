# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0009_remove_dropofftime_neighborhood'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neighborhood',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
