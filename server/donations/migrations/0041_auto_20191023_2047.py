# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import donations.models
import enumfields.fields
import rules.contrib.models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0040_auto_20191023_2038'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AppointmentTime',
            new_name='Event',
        ),
    ]
