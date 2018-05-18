from collections import defaultdict
from rest_framework import serializers

from donations.models import Category, DonationFulfillment, DonationRequest, Item


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


class DonationRequestListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        results = super(DonationRequestListSerializer, self).to_representation(instance)
        results_count = defaultdict(lambda: defaultdict(int))
        from collections import OrderedDict

        for result in results:
            item = result['item']
            item_type = item['tag']
            category = item['category_tag']
            results_count[category][item_type] += 1

        requests = []

        for item in Item.objects.order_by('tag'):
            requests.append(
                {
                    'type': item.tag,
                    'category': item.category.tag,
                    'count': results_count[item.category.tag][item.tag],
                }
            )


        return requests


class DonationRequestPublicSerializer(serializers.ModelSerializer):
    item = ItemRequestSerializer()

    class Meta:
        model = DonationRequest
        fields = (
            'id', 'item', 'size', 'created', 'city'
        )
        list_serializer_class = DonationRequestListSerializer
