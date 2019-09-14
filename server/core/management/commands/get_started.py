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
from organizations.models import Org, OrgUserRole, OrgUserRoleType

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

    def create_orgs(self):
        orgs = []

        for _ in range(DEMO_OBJECT_COUNT):
            org = Org(
                name=fake.company(),
                email=fake.email(),
                ein=fake.ein(),
                street_address_1=fake.street_address(),
                city='Los Angeles',
                state='CA',
                phone=fake.e164(region_code='US', valid=True, possible=True),
                zipcode=fake.postcode_in_state(state_abbr='CA'),
            )

            orgs.append(org)

        Org.objects.bulk_create(orgs)

        return orgs

    def create_org_users(self, ignore_duplicates=False):
        org_users = []
        org_user_roles = []
        count = 1

        for _ in range(DEMO_OBJECT_COUNT):
            org_user = User(
                display_name=fake.first_name(),
                email='org_user_{}@example.com'.format(count),
                is_staff=True,
                is_active=False,
            )

            count += 1
            org_users.append(org_user)

        try:
            User.objects.bulk_create(org_users)
        except IntegrityError:
            if not ignore_duplicates:
                raise CommandError('Existing user(s) found')
            else:
                self.stdout.write(self.style.WARNING('Duplicate users found, skipping'))
                return None

        count = 0

        for org_user in org_users:
            # Set password (must be done after bulk create)
            org_user.set_password('password')
            org_user.save()

            org_user_role = OrgUserRole(
                type=OrgUserRoleType.ADMIN,
                user=org_user,
                org=self.orgs[count % len(self.orgs)]
            )

            count += 1
            org_user_roles.append(org_user_role)

        OrgUserRole.objects.bulk_create(org_user_roles)

        return org_users

    def create_locations(self, neighborhoods):
        locations = []
        count = 0

        for _ in range(DEMO_OBJECT_COUNT):
            neighborhood = random.choice(neighborhoods)

            location = Location(
                location_name=fake.company(),
                neighborhood=neighborhood,
                street_address_1=fake.street_address(),
                city='Los Angeles',
                state='CA',
                phone=fake.e164(region_code='US', valid=True, possible=True),
                zipcode=fake.postcode_in_state(state_abbr='CA'),
                org=self.orgs[count % len(self.orgs)]
            )

            count += 1
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

    def load_demo_data(self, ignore_duplicates=False):
        neighborhoods = Neighborhood.objects.all()

        self.orgs = self.create_orgs()
        self.stdout.write(self.style.SUCCESS('Successfully create %s orgs' % len(self.orgs)))

        org_users = self.create_org_users(ignore_duplicates=ignore_duplicates)
        if org_users:
            self.stdout.write(self.style.SUCCESS('Successfully created %s org users' % len(org_users)))

        locations = self.create_locations(neighborhoods)
        self.stdout.write(self.style.SUCCESS('Successfully created %s locations' % len(locations)))

        dropoff_times = self.create_dropoff_times(locations)
        self.stdout.write(self.style.SUCCESS('Successfully created %s dropoff times' % len(dropoff_times)))

    def handle(self, *args, **options):
        if settings.DEBUG is True:
            if not options['no_migrations']:
                call_command('migrate')
            try:
                User.objects.create_superuser(
                    'admin@example.com', 'password',
                    display_name='Admin')

                self.stdout.write(self.style.SUCCESS("You are migrated and have an admin user"))
                self.stdout.write(self.style.SUCCESS("Email: admin@example.com"))
                self.stdout.write(self.style.SUCCESS("Password: password"))

            except IntegrityError:
                if not options['ignore_duplicates']:
                    raise CommandError("User admin@example.com already exists")

            if not options['skip_demo_data']:
                self.stdout.write(self.style.SUCCESS('Loading demo data...'))
                self.load_demo_data(ignore_duplicates=options['ignore_duplicates'])
            else:
                self.stdout.write(self.style.WARNING('Skipping demo data...'))
        else:
            raise CommandError("Command can only be run in debug mode")
