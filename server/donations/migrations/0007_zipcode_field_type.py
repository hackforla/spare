# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 23:42
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0006_donationfulfillment_pickup_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='zipcode',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(code='invalid_zipcode', message='Invalid zip code format (must be 5 or 9 digits)')]),
        ),
    ]
