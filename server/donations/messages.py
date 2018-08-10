
from core.sms.message import SMSMessage


class RequestSMSBase(SMSMessage):
    def get_to(self):
        return self.instance.phone

    def get_context_data(self):
        instance = self.instance

        return {
            'name': instance.name,
            'item': instance.item.display_name.lower()
        }


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


class FulfillmentRequestorSMS(FulfillmentRequestorSMSBase):
    msg = (
        "Great news, {{ requestor_name }}! Your request for {{ item }} has been fulfilled. "
        "We'll put you in touch with {{ donator_name }} to pick up the item."
    )


EMAIL_MESSAGE_TEMPLATES = {
    'requestor_request_received': 'requestors/request_received.html',
    'requestor_request_fulfilled': 'requestors/request_fulfilled.html',
    'donator_fulfillment_received': 'donators/fulfillment_received.html'
}
