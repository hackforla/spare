# -*- coding: utf-8 -*-
"""A mgmt command for new users to get them migrated and setup with an admin
user.

Not to be run in production!
"""

from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.core.management import call_command
from core.models import User

from django.conf import settings
from django.db.utils import IntegrityError

class Command(BaseCommand):
    help = 'Create an admin for development purposes'


    def handle(self, *args, **options):

        if settings.DEBUG is True:
            call_command('migrate')
            try:
                User.objects.create_superuser('admin@example.com', 'password')
            except IntegrityError:
                pass

            self.stdout.write(self.style.SUCCESS("You are migrated and have an admin user"))
            self.stdout.write(self.style.SUCCESS("Email: admin@example.com"))
            self.stdout.write(self.style.SUCCESS("Password: password"))
