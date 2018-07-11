import random

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from donations.models import DonationRequest, DonationFulfillment

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
        if instance.email:
            send_mail(
                'Thank you for your request!',
                f"Thank you {instance.name}! We've received your request for {instance.item} and we'll let you know when one becomes available.",
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,
            )
        else:
            pass

@receiver(post_save, sender=DonationFulfillment)
def donation_fulfilled_email(sender, instance, created, **kwargs):
    if (created):
        requestor_email = instance.request.email
        if requestor_email:
            send_mail(
                'Your request has been fulfilled!',
                f"Great news, {instance.request.name}! Your request for {instance.request.item} has been fulfilled. We'll put you in touch with {instance.name} to pick up the item.",
                settings.DEFAULT_FROM_EMAIL,
                [requestor_email],
                fail_silently=False,
            )
        else:
            pass

        donator_email = instance.email
        if donator_email:
            send_mail(
                'Thank you for your donation!',
                f"Thank you {instance.name}! We'll set you up to donate your {instance.request.item} to {instance.request.name}.",
                settings.DEFAULT_FROM_EMAIL,
                [donator_email],
                fail_silently=False,
            )
        else:
            pass
