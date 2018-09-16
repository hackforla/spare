import logging

from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from core.sms.backends.base import BaseSMSBackend

logger = logging.getLogger(__name__)

client = Client(
    settings.TWILIO_ACCOUNT_ID,
    settings.TWILIO_AUTH_TOKEN
)

class SMSBackend(BaseSMSBackend):
    def send_message(self, message):
        message = client.messages.create(
            body=message.body,
            from_=self.from_,
            to=message.to
        )
        logger.info(message.body,
            extra={
            'from_': self.from_,
            'sid': message.sid,
            'status': message.status,
            'to':message.to,
            'dt': timezone.now()
            }
        )
