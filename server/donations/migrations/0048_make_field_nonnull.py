# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-10-28 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0047_remove_invalid_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donorappointment',
            name='fulfillment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donor_appointments', to='donations.Fulfillment'),
        ),
    ]
