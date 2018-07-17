from django.conf import settings
from django.template import Context, Template
from django.utils.module_loading import import_string


class SMSMessage:
    _backend = None
    msg = ''

    def __init__(self, instance):
        self._backend = import_string(settings.SMS_BACKEND)()
        self.instance = instance
        self.to = self.get_to()

        if not self.msg:
            raise ValueError("Missing 'msg' value")

        # TODO: Raise/log error if invalid 'to' phone number
        self.render()

    def get_context_data(self):
        return {}

    def render(self):
        template = Template(self.msg)
        context = self.get_context_data()
        self.body = template.render(Context(context))

    def send(self):
        self._backend.send_message(
            self
        )
