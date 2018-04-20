# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from donations.models import DEFAULT_CATEGORIES_AND_ITEMS


def create_default_categories_and_items(apps, schema_editor):
    Category = apps.get_model('donations', 'Category')
    Item = apps.get_model('donations', 'Item')

    for (category_tag, category_display_name), items in DEFAULT_CATEGORIES_AND_ITEMS.items():
        # For each category, add category if it doesn't exist
        category = Category.objects.filter(tag=category_tag).first()
        if not category:
            category = Category.objects.create(
                tag=category_tag,
                display_name=category_display_name
            )

        # For each set of category items, add item if doesn't exist
        for item_tag, item_display_name in items:
            item = Item.objects.filter(tag=item_tag).first()
            if not item:
                Item.objects.create(
                    tag=item_tag,
                    display_name=item_display_name,
                    category=category
                )


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_default_categories_and_items,
            migrations.RunPython.noop
        )
    ]
