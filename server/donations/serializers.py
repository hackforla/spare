from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from donations.models import (
    DonationFulfillment, DonationRequest, DropoffTime, Item, Location,
    Neighborhood
)


class ContactInfoValidator(object):
    def __call__(self, value):
        if not (value.get('phone') or value.get('email')):
            raise serializers.ValidationError('You must provide either email address or phone number.')

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)


class DropoffValidator(object):
    def __call__(self, value):
        dropoff_time = value.get('dropoff_time')
        dropoff_date = value.get('dropoff_date')
        manual_dropoff_date = value.get('manual_dropoff_date')

        if dropoff_time:
            if not dropoff_date:
                raise serializers.ValidationError('Drop off date require')
            elif dropoff_time.day.value != dropoff_date.weekday():
                raise serializers.ValidationError('Date provided does not match dropoff time date')

            start_datetime = timezone.make_aware(
                datetime.combine(dropoff_date, dropoff_time.time_start)
            )

            if start_datetime < timezone.now():
                raise serializers.ValidationError('Cannot schedule dropoff for past date')

            if (start_datetime - timezone.now()) > timedelta(weeks=12):
                raise serializers.ValidationError('Cannot schedule dropoff more than 12 weeks in future')

        elif manual_dropoff_date:
            if dropoff_date:
                raise serializers.ValidationError('Cannot provide both manual dropoff date and dropoff date')

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
            'id', 'name', 'phone', 'email', 'request', 'dropoff_time', 'dropoff_date',
            'manual_dropoff_date', 'created', 'code'
        )
        read_only_fields = (
            'id', 'created',
        )
        # TODO: Add validator to raise error when request has already been fulfilled
        #       (currently raises vague 'object does not exist' error)
        validators = [ContactInfoValidator(), DropoffValidator()]
        extra_kwargs = {
            'email': {'required': True},
        }


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = (
            'id', 'name',
        )


class DonationRequestSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(
        slug_field='tag',
        queryset=Item.objects.all()
    )

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
            'street_address_2', 'city', 'state', 'zipcode', 'phone', 'website', 'maps_url'
        )


class DropoffTimeListSerializer(serializers.ListSerializer):
    def to_representation(self, items):
        data = []

        for item in items:
            if hasattr(item, 'get_visible_dates'):
                for date in item.get_visible_dates():
                    child_data = self.child.to_representation(item)
                    child_data['date'] = date
                    child_data['type'] = 'recurring'
                    data.append((date, child_data))
            else:
                child_data = self.child.to_representation(item)
                child_data['date'] = item.dropoff_date
                child_data['type'] = 'manual'
                data.append((item.dropoff_date, child_data))

        return [dropoff_data for _, dropoff_data in sorted(data, key=lambda item: item[0])]


class DropoffTimeSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    location = LocationSerializer()
    date = serializers.DateField(read_only=True)
    time_start = serializers.TimeField(read_only=True)
    time_end = serializers.TimeField(read_only=True)

    class Meta:
        list_serializer_class = DropoffTimeListSerializer
