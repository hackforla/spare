from rest_framework import serializers

from donations.models import DonationFulfillment, DonationRequest, Item


class ContactInfoValidator(object):
    def __call__(self, value):
        if not (value.get('phone') or value.get('email')):
            raise serializers.ValidationError('You must provide either email address or phone number.')

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)


class ItemRequestSerializer(serializers.ModelSerializer):
    category_tag = serializers.CharField(source='category.tag')
    category_display_name = serializers.CharField(source='category.display_name')

    class Meta:
        model = Item
        fields = (
            'id', 'tag', 'display_name', 'category_tag', 'category_display_name'
        )
        read_only_fields = (
            'id', 'tag', 'display_name', 'category_tag', 'category_display_name'
        )


class DonationFulfillmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationFulfillment
        fields = (
            'id', 'name', 'phone', 'email', 'request', 'created'
        )
        read_only_fields = (
            'id', 'created',
        )
        validators = [ContactInfoValidator()]


class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = (
            'id', 'name', 'phone', 'email', 'item', 'size', 'code',
            'created'
        )
        read_only_fields = (
            'id', 'created', 'code'
        )
        validators = [ContactInfoValidator()]


class DonationRequestPublicSerializer(serializers.ModelSerializer):
    item = ItemRequestSerializer()

    class Meta:
        model = DonationRequest
        fields = (
            'id', 'item', 'size', 'created'
        )
