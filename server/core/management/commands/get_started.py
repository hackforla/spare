# -*- coding: utf-8 -*-
"""A mgmt command for new users to get them migrated and setup with an admin
user.

Not to be run in production!
"""

from __future__ import unicode_literals

import datetime
import random

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from faker import Faker
from faker_e164.providers import E164Provider

from core.models import User
from donations.models import DaysOfWeek, DropoffTime, Location, Neighborhood

fake = Faker()
fake.add_provider(E164Provider)


DEMO_OBJECT_COUNT = 10


class Command(BaseCommand):
    help = 'Create an admin for development purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-migrations', action='store_true', help='Skip running migrations')
        parser.add_argument(
            '--skip-demo-data', action='store_true', help='Skip creating demo data')
        parser.add_argument(
            '--ignore-duplicates', action='store_true', help='Ignore duplicate objects')

    def create_locations(self, neighborhoods):
        locations = []

        for _ in range(DEMO_OBJECT_COUNT):
            neighborhood = random.choice(neighborhoods)

            location = Location(
                organization_name=fake.company(),
                location_name=fake.company(),
                neighborhood=neighborhood,
                street_address_1=fake.street_address(),
                city='Los Angeles',
                state='CA',
                phone=fake.e164(region_code='US', valid=True, possible=True),
                zipcode=fake.postcode_in_state(state_abbr='CA'),
            )

            locations.append(location)

        Location.objects.bulk_create(locations)

        return locations

    def create_dropoff_times(self, locations):
        dropoff_times = []

        for _ in range(DEMO_OBJECT_COUNT):
            location = random.choice(locations)

            # Restrict test start times from 6AM-6PM
            valid_start_times = range(6, 18)

            start_hour = random.choice(valid_start_times)
            end_hour = start_hour + 1

            dropoff_time = DropoffTime(
                time_start=datetime.time(hour=start_hour),
                time_end=datetime.time(hour=end_hour),
                location=location,
                day=random.choice(list(DaysOfWeek))
            )

            dropoff_times.append(dropoff_time)

        DropoffTime.objects.bulk_create(dropoff_times)

        return dropoff_times

    def load_demo_data(self):
        neighborhoods = Neighborhood.objects.all()

        locations = self.create_locations(neighborhoods)
        self.stdout.write(self.style.SUCCESS('Successfully created %s locations' % len(locations)))

        dropoff_times = self.create_dropoff_times(locations)
        self.stdout.write(self.style.SUCCESS('Successfully created %s dropoff times' % len(dropoff_times)))

    def handle(self, *args, **options):
        if settings.DEBUG is True:
            if not options['no_migrations']:
                call_command('migrate')
            try:
                User.objects.create_superuser('admin@example.com', 'password')

                self.stdout.write(self.style.SUCCESS("You are migrated and have an admin user"))
                self.stdout.write(self.style.SUCCESS("Email: admin@example.com"))
                self.stdout.write(self.style.SUCCESS("Password: password"))

            except IntegrityError:
                if not options['ignore_duplicates']:
                    raise CommandError("User admin@example.com already exists")

            if not options['skip_demo_data']:
                self.stdout.write(self.style.SUCCESS('Loading demo data...'))
                self.load_demo_data()
            else:
                self.stdout.write(self.style.WARNING('Skipping demo data...'))
        else:
            raise CommandError("Command can only be run in debug mode")
