from django.conf import settings


class BaseSMSBackend:
    # Kind of a necessary abstraction, but meant to be somewhat in line
    # with Django email backends
    from_ = None

    def __init__(self):
        self.from_ = settings.SMS_FROM_NUMBER

    def send_message(self, message):
        raise NotImplementedError('subclasses of BaseSMSBackend must override send_messages() method')
