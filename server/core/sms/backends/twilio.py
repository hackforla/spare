from django.conf import settings
from twilio.rest import Client

from core.sms.backends.base import BaseSMSBackend

client = Client(
    settings.TWILIO_ACCOUNT_ID,
    settings.TWILIO_AUTH_TOKEN
)


class SMSBackend(BaseSMSBackend):
    def send_message(self, message):
        # TODO: Add logging
        client.messages.create(
            body=message.body,
            from_=self.from_,
            to=message.to
        )
