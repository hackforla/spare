# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from donations.models import DEFAULT_NEIGHBORHOODS


def create_default_neighborhoods(apps, schema_editor):
    Neighborhood = apps.get_model('donations', 'Neighborhood')

    for neighborhood in DEFAULT_NEIGHBORHOODS:
        Neighborhood.objects.get_or_create(name=neighborhood)


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0011_dropofftime_day'),
    ]

    operations = [
        migrations.RunPython(
            create_default_neighborhoods,
            migrations.RunPython.noop
        )
    ]
