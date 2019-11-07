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

    def display_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def display_warning(self, message):
        self.stdout.write(self.style.WARNING(message))

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-migrations', action='store_true', help='Skip running migrations')
        parser.add_argument(
            '--skip-demo-data', action='store_true', help='Skip creating demo data')

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

    def create_org_users(self):
        org_users = []
        org_user_roles = []
        count = 1

        for _ in range(DEMO_OBJECT_COUNT):
            org_user = User(
                display_name=fake.first_name(),
                email='org_user_{}@example.com'.format(count),
                is_staff=True,
                is_active=True,
            )

            count += 1
            org_users.append(org_user)

        try:
            User.objects.bulk_create(org_users)
        except IntegrityError:
            self.display_warning('Duplicate users found, skipping')
            return

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

        self.display_success('Successfully created %s org users' % len(org_users))

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

    def load_demo_data(self):
        neighborhoods = Neighborhood.objects.all()

        self.orgs = self.create_orgs()
        self.display_success('Successfully create %s orgs' % len(self.orgs))

        self.create_org_users()

        locations = self.create_locations(neighborhoods)
        self.display_success('Successfully created %s locations' % len(locations))

        dropoff_times = self.create_dropoff_times(locations)
        self.display_success('Successfully created %s dropoff times' % len(dropoff_times))

    def create_admin(self):
        user = User.objects.create_superuser(
            'admin@example.com', 'password',
            display_name='Admin')

        self.display_success("An admin user has been created")
        self.display_success("Email: admin@example.com")
        self.display_success("Password: password")

        return user

    def handle(self, *args, **options):
        if settings.DEBUG is True:
            if not options['no_migrations']:
                call_command('migrate')
            try:
                self.create_admin()

            except IntegrityError:
                self.display_warning("User admin@example.com already exists")

            if not options['skip_demo_data']:
                self.display_success('Loading demo data...')
                self.load_demo_data()
            else:
                self.warning('Skipping demo data...')
        else:
            raise CommandError("Command can only be run in debug mode")
