import pytest

from donations.messages import FulfillmentRequestorSMS
from donations.tasks import send_request_confirmation_message


@pytest.mark.django_db
def test_locmem_sms_backend(smsoutbox, donation_fulfillment):
    assert not smsoutbox

    message = FulfillmentRequestorSMS(
        instance=donation_fulfillment
    )

    message.send()

    assert len(smsoutbox) == 1
    assert smsoutbox[0] == message


@pytest.mark.django_db
def test_send_request_confirmation_message(smsoutbox, mailoutbox, donation_request):
    assert not smsoutbox
    assert not mailoutbox

    # Verify that email is set
    assert donation_request.email

    send_request_confirmation_message(donation_request)

    # Mail should have been sent, but no sms
    assert len(smsoutbox) == 0
    assert len(mailoutbox) == 1

    # Removing email should now send sms
    donation_request.email = ''
    donation_request.save()

    # Reset mail outbox
    mailoutbox = []

    send_request_confirmation_message(donation_request)

    assert len(smsoutbox) == 1
    assert len(mailoutbox) == 0


# TODO: Add tests for message contests
