from core import sms
from core.sms.backends.base import BaseSMSBackend


class SMSBackend(BaseSMSBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(sms, 'outbox'):
            sms.outbox = []

    def send_message(self, message):
        if not hasattr(sms, 'outbox'):
            sms.outbox = []
        else:
            sms.outbox.append(message)
