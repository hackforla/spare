from django.conf import settings
from donations.messages import (
    DonationRequestReceivedEmail, DonationRequestReceivedSMS,
    FulfillmentDonatorConfirmationEmail, FulfillmentRequestorEmail,
    FulfillmentRequestorSMS, EMAIL_MESSAGE_TEMPLATES
)
from templated_email import send_templated_mail


def send_email_message(message_name, to_email, context=None):
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
                'item_size': instance.size or 'N/A',

                'location_name': 'The Shower of Hope',
                'neighborhood': instance.neighborhood.name,
            },
        )
    elif instance.phone:
        DonationRequestReceivedSMS(instance=instance).send()


def send_fulfillment_confirmation_messages(instance):
    fulfillment = instance
    request = fulfillment.request
    location = fulfillment.dropoff_time.location

    if fulfillment.email:
        send_email_message(
            'donator_fulfillment_received',
            fulfillment.email,
            context={
                'item_type': request.item.display_name,
                'item_size': request.size or 'N/A',

                'location_name': 'The Shower of Hope',
                'location_address_1': location.street_address_1,
                'location_address_2': location.street_address_2,
                'location_city': location.city,
                'location_state': location.state,
                'location_zipcode': location.zipcode,
                'neighborhood': request.neighborhood.name,

                'requestor_name': request.name,
                'requestor_email': request.email,
                'requestor_phone': request.phone,

                'dropoff_date': fulfillment.dropoff_date,
                'dropoff_time': fulfillment.dropoff_time.time_start,
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
                'item_size': request.size or 'N/A',

                'location_name': 'The Shower of Hope',
                'location_address_1': location.street_address_1,
                'location_address_2': location.street_address_2,
                'location_city': location.city,
                'location_state': location.state,
                'location_zipcode': location.zipcode,
                'neighborhood': request.neighborhood.name,

                'dropoff_date': fulfillment.dropoff_date,
                'dropoff_time': fulfillment.dropoff_time.time_start,
            },
        )
    elif instance.request.phone:
        FulfillmentRequestorSMS(instance=instance).send()
