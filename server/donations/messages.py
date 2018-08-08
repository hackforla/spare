from django.core.mail.message import EmailMessage
from django.template import Context, Template

from core.sms.message import SMSMessage


class EmailBase(EmailMessage):
    msg = ''
    subject = ''

    def __init__(self, instance):
        self.instance = instance
        self._subject = self.subject
        super().__init__(to=[self.get_to()])
        self.render()

    def render(self):
        context = Context(self.get_context_data())
        self.body = Template(self.msg).render(context)
        self.subject = Template(self._subject).render(context)

    def send(self):
        super().send()

    def get_to(self):
        raise NotImplementedError('subclass of EmailBase must define get_to method')

    def get_context_data(self):
        raise NotImplementedError('subclass of EmailBase must define get_context_data method')


class RequestEmailBase(EmailBase):
    def get_to(self):
        return self.instance.email

    def get_context_data(self):
        instance = self.instance

        return {
            'name': instance.name,
            'item': instance.item.display_name.lower()
        }


class RequestSMSBase(SMSMessage):
    def get_to(self):
        return self.instance.phone

    def get_context_data(self):
        instance = self.instance

        return {
            'name': instance.name,
            'item': instance.item.display_name.lower()
        }


class FulfillmentEmailBase(EmailBase):
    def get_context_data(self):
        instance = self.instance

        return {
            'requestor_name': instance.request.name,
            'donator_name': instance.name,
            'item': instance.request.item.display_name.lower(),
        }


class FulfillmentRequestorEmailBase(FulfillmentEmailBase):
    def get_to(self):
        return self.instance.request.email


class FulfillmentDonatorEmailBase(FulfillmentEmailBase):
    def get_to(self):
        return self.instance.email


class FulfillmentRequestorSMSBase(SMSMessage):
    def get_to(self):
        return self.instance.request.phone

    def get_context_data(self):
        instance = self.instance

        return {
            'requestor_name': instance.request.name,
            'donator_name': instance.name,
            'item': instance.request.item.display_name.lower(),
        }


class DonationRequestReceivedSMS(RequestSMSBase):
    msg = (
        "Thank you {{ name }}! We've received your request for {{ item }} "
        "and we'll let you know when one becomes available."
    )


class DonationRequestReceivedEmail(RequestEmailBase):
    subject = 'Your request has been received!'

    msg = (
        "Thank you {{ name }}! We've received your request for {{ item }} "
        "and we'll let you know when one becomes available."
    )


class FulfillmentRequestorSMS(FulfillmentRequestorSMSBase):
    msg = (
        "Great news, {{ requestor_name }}! Your request for {{ item }} has been fulfilled. "
        "We'll put you in touch with {{ donator_name }} to pick up the item."
    )


class FulfillmentRequestorEmail(FulfillmentRequestorEmailBase):
    subject = "Your request has been fulfilled!"
    msg = (
        "Great news, {{ requestor_name }}! Your request for {{ item }} has been fulfilled. "
        "We'll put you in touch with {{ donator_name }} to pick up the item."
    )


class FulfillmentDonatorConfirmationEmail(FulfillmentDonatorEmailBase):
    subject = "Thank you for your donation!"
    msg = (
        "Thank you {{ donator_name }}! We'll set you up to donate your {{ item }} "
        "to {{ requestor_name }}."
    )

EMAIL_MESSAGE_TEMPLATES = {
    'requestor_request_received': 'requestors/request_received.html',
    'requestor_request_fulfilled': 'requestors/request_fulfilled.html',
    'donator_fulfillment_received': 'donators/fulfillment_received.html'
}
