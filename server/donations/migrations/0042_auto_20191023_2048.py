# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-24 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0041_auto_20191023_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dropofftime',
            name='location',
        ),
        migrations.RemoveField(
            model_name='manualdropoffdate',
            name='location',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='appointment_time',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='donationrequest',
            old_name='valid_appointment_times',
            new_name='valid_events',
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='donations.Location'),
        ),
        migrations.DeleteModel(
            name='DropoffTime',
        ),
        migrations.DeleteModel(
            name='ManualDropoffDate',
        ),
    ]
