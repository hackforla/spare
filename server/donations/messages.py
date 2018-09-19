
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
            'location': instance.location,
            'start_time': instance.time_start,
            'end_time': instance.time_end,
            'date': instance.date
        }


class DonationRequestReceivedSMS(RequestSMSBase):
    msg = (
        "Thank you {{ name }}! We've received your request for {{ item }} "
        "and we'll let you know when one becomes available."
    )


class FulfillmentRequestorSMS(FulfillmentRequestorSMSBase):
    msg = (
        "Your request for {{ item }} has been fulfilled. Please be at {{ location.street_address_1 }}"
        "{% if location.street_address_2 %} {{ location.street_address_2 }}{% endif %}, {{ location.city }}, "
        "at {{ start_time }} on {{ date }} to pick up your item."
    )


EMAIL_MESSAGE_TEMPLATES = {
    'requestor_request_received': 'requestors/request_received.html',
    'requestor_request_fulfilled': 'requestors/request_fulfilled.html',
    'donator_fulfillment_received': 'donators/fulfillment_received.html'
}
