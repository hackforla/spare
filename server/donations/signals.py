import random

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from donations.models import Request, DonorAppointment
from donations.tasks import (
    send_donor_appointment_confirmation_messages, send_request_confirmation_message
)


@receiver(post_save, sender=Request)
def donation_created_email(sender, instance, created, **kwargs):
    if (created):
        send_request_confirmation_message(instance)


@receiver(post_save, sender=DonorAppointment)
def send_donor_appointment_confirmation_email(sender, instance, created, **kwargs):
    if (created):
        send_donor_appointment_confirmation_messages(instance)
