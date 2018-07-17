import random

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from core.queues import enqueue
from donations.models import DonationFulfillment, DonationRequest
from donations.tasks import (
    send_fulfillment_confirmation_messages, send_request_confirmation_message
)

# TODO: Use better words
NOUNS = (
    'area', 'book', 'business', 'case', 'child', 'company', 'country',
    'day', 'eye', 'fact', 'family', 'government', 'group', 'hand', 'home',
    'job', 'life', 'lot', 'man', 'money', 'month', 'mother', 'night',
    'number', 'part', 'people', 'place', 'point', 'problem', 'program',
    'question', 'right', 'room', 'school', 'state', 'story', 'student',
    'study', 'system', 'thing', 'time', 'water', 'way', 'week', 'woman',
    'word', 'work', 'world', 'year',
)


@receiver(pre_save, sender=DonationRequest)
def create_code(sender, instance, **kwargs):
    attempts = 0
    if not instance.code:
        while True and attempts < 10:
            seen = []
            while (len(seen) < 4):
                word = random.choice(NOUNS).capitalize()
                if word not in seen:
                    seen.append(word)

            code = ''.join(seen)

            if not DonationRequest.objects.filter(code=code).exists():
                instance.code = code
                break

            attempts += 1

    if not instance.code:
        raise ValidationError('Unable to generate unique code for this request.')


@receiver(post_save, sender=DonationRequest)
def donation_created_email(sender, instance, created, **kwargs):
    if (created):
        enqueue(send_request_confirmation_message, instance)


@receiver(post_save, sender=DonationFulfillment)
def donation_fulfilled_email(sender, instance, created, **kwargs):
    if (created):
        enqueue(send_fulfillment_confirmation_messages, instance)
