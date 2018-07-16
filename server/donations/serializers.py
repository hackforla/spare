from rest_framework import serializers

from donations.models import DonationFulfillment, DonationRequest, Item, Neighborhood, Location, DropoffTime


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
    code = serializers.CharField(source='request.code', read_only=True)
    request = serializers.PrimaryKeyRelatedField(
        queryset=DonationRequest.unfulfilled.all()
    )

    class Meta:
        model = DonationFulfillment
        fields = (
            'id', 'name', 'phone', 'email', 'request', 'dropoff_time', 'created', 'code'
        )
        read_only_fields = (
            'id', 'created',
        )
        # TODO: Add validator to raise error when request has already been fulfilled
        #       (currently raises vague 'object does not exist' error)
        validators = [ContactInfoValidator()]


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = (
            'id', 'name',
        )


class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationRequest
        fields = (
            'id', 'name', 'phone', 'email', 'item', 'size', 'neighborhood', 'code',
            'created'
        )
        read_only_fields = (
            'id', 'created', 'code'
        )
        validators = [ContactInfoValidator()]


class DonationRequestPublicSerializer(serializers.ModelSerializer):
    item = ItemRequestSerializer()
    neighborhood = NeighborhoodSerializer()

    class Meta:
        model = DonationRequest
        fields = (
            'id', 'item', 'size', 'neighborhood', 'created',
        )


class LocationSerializer(serializers.ModelSerializer):
    neighborhood = NeighborhoodSerializer()

    class Meta:
        model = Location
        fields = (
            'organization_name', 'location_name', 'neighborhood', 'street_address_1',
            'street_address_2', 'city', 'state', 'zipcode', 'phone', 'website'
        )


class DropoffTimeListSerializer(serializers.ListSerializer):
    def to_representation(self, items):
        data = []

        for item in items:
            for date in item.get_visible_dates():
                child_data = self.child.to_representation(item)
                child_data['date'] = date
                data.append(child_data)

        return data


class DropoffTimeSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = DropoffTime
        fields = (
            'id', 'time_start', 'time_end', 'location',
        )
        read_only_fields = (
            'id', 'time_start', 'time_end', 'location',
        )
        list_serializer_class = DropoffTimeListSerializer
