# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-19 19:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0031_appointmenttime_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemtype',
            old_name='verbose_name',
            new_name='inline_text_name',
        ),
        migrations.AlterField(
            model_name='appointmenttime',
            name='cancelled',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='appointmenttime',
            name='end_time',
            field=models.TimeField(blank=True),
        ),
    ]
