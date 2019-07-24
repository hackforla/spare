from django.conf import settings
from templated_email import send_templated_mail

from core.utils import is_test_email
from donations.messages import (
    DonationRequestReceivedSMS, EMAIL_MESSAGE_TEMPLATES,
    FulfillmentRequestorSMS
)


def send_email_message(message_name, to_email, context=None):
    DEV_BACKENDS = [
        'django.core.mail.backends.console.EmailBackend',
        'django.core.mail.backends.locmem.EmailBackend'
    ]

    if (settings.EMAIL_BACKEND in DEV_BACKENDS) or (not is_test_email(to_email)):
        send_templated_mail(
            template_name=EMAIL_MESSAGE_TEMPLATES[message_name],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            context=context or {}
        )


def send_request_confirmation_message(instance):
    if instance.email:
        send_email_message(
            'requestor_request_received',
            instance.email,
            context={
                'item_type': instance.item.display_name,
                'item_size': instance.size,

                'neighborhood': instance.neighborhood.name,
            },
        )
    elif instance.phone:
        DonationRequestReceivedSMS(instance=instance).send()


def send_fulfillment_confirmation_messages(instance):
    fulfillment = instance
    request = fulfillment.request
    location = fulfillment.location

    if fulfillment.email:
        send_email_message(
            'donator_fulfillment_received',
            fulfillment.email,
            context={
                'item_type': request.item.display_name,
                'item_size': request.size,

                'location_name': location.location_name,
                'location_address_1': location.street_address_1,
                'location_address_2': location.street_address_2,
                'location_city': location.city,
                'location_state': location.state,
                'location_zipcode': location.zipcode,
                'location_maps_url': location.maps_url,
                'location_notes': location.notes,
                'neighborhood': request.neighborhood.name,

                'requestor_name': request.name,

                'dropoff_date': fulfillment.date,
                'dropoff_time': fulfillment.time_start,
            },
        )
    else:
        # TODO: Currently, we do nothing here in order to preserve texts
        #       for those requesting items.
        pass

    if request.email:
        send_email_message(
            'requestor_request_fulfilled',
            request.email,
            context={
                'item_type': request.item.display_name,
                'item_size': request.size,

                'location_name': location.location_name,
                'location_address_1': location.street_address_1,
                'location_address_2': location.street_address_2,
                'location_city': location.city,
                'location_state': location.state,
                'location_zipcode': location.zipcode,
                'location_maps_url': location.maps_url,
                'location_notes': location.notes,
                'neighborhood': request.neighborhood.name,

                'donator_name': fulfillment.name,

                'dropoff_date': fulfillment.date,
                'dropoff_time': fulfillment.time_start,
            },
        )
    elif instance.request.phone:
        FulfillmentRequestorSMS(instance=instance).send()
