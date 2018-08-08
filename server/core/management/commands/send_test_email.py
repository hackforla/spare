# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.management.base import BaseCommand


from donations.tasks import send_email_message
from donations.messages import EMAIL_MESSAGE_TEMPLATES


TEST_CONTEXT = {
    # Request info
    'item_type': 'Shirt',
    'item_size': 'XL',
    'requestor_name': 'Jimbo',
    'requestor_email': 'jimbojones@example.com',
    'requestor_phone': '+15556667777',

    # Dropoff info
    'location_name': 'The Shower of Hope',
    'location_address_1': '123 Fake St',
    'location_address_2': 'Suite 200',
    'location_city': 'Los Angeles',
    'location_state': 'CA',
    'location_zip': '90000',
    'neighborhood': 'Highland Park',
    'dropoff_date': 'Saturday, August 25th, 2018',
    'dropoff_time': '11AM',
}


class Command(BaseCommand):
    help = 'Send a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            'email',
            type=str,
            help='Email address to send email',
        )

        parser.add_argument(
            'message_name',
            type=str,
            help='Name of email message to send',
        )

    def handle(self, *args, **options):
        email = options['email']
        message_name = options['message_name']

        if message_name not in EMAIL_MESSAGE_TEMPLATES:
            print("\nMessage name '{}' not a valid message name".format(message_name))
            print("\tOptions are: {}\n".format(", ".join(EMAIL_MESSAGE_TEMPLATES.keys())))

        send_email_message(
            message_name,
            email,
            context=TEST_CONTEXT
        )
