# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-12 02:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0018_location_changes'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationfulfillment',
            name='specified_dropoff_time',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specified_dropoff_time', to='donations.DropoffTime', verbose_name='Specified Dropoffs'),
        ),
        migrations.AlterField(
            model_name='donationfulfillment',
            name='dropoff_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donations.DropoffTime', verbose_name='Recurring Dropoffs'),
        ),
    ]
