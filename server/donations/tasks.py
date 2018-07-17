from donations.messages import (
    DonationRequestReceivedEmail, DonationRequestReceivedSMS,
    FulfillmentDonatorConfirmationEmail, FulfillmentRequestorEmail,
    FulfillmentRequestorSMS
)


def send_request_confirmation_message(instance):
    if instance.email:
        DonationRequestReceivedEmail(instance=instance).send()
    elif instance.phone:
        DonationRequestReceivedSMS(instance=instance).send()


def send_fulfillment_confirmation_messages(instance):
    if instance.request.email:
        FulfillmentRequestorEmail(instance=instance).send()
    elif instance.request.phone:
        FulfillmentRequestorSMS(instance=instance).send()

    if instance.email:
        FulfillmentDonatorConfirmationEmail(instance=instance).send()
    else:
        # TODO: Currently, we do nothing here in rrder to preserve texts
        #       for those requesting items.
        pass
