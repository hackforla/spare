from core.sms.backends.base import BaseSMSBackend


class SMSBackend(BaseSMSBackend):
    def send_message(self, message):
        msg = (
            "From: {from_}\n"
            "To: {to}\n"
            "Message: {message}\n"
        ) + ('-' * 79) + "\n"

        print(
            msg.format(
                to=message.to,
                from_=self.from_,
                message=message.body,
            )
        )
