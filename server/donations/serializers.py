from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from donations.models import (
    Request, Location, Neighborhood, RequestItem,
    Subcategory, Event, ScheduleType, Category, Subcategory
)


class ContactInfoValidator:
    def __call__(self, value):
        if not (value.get('phone') or value.get('email')):
            raise serializers.ValidationError('You must provide either email address or phone number.')

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)


# class DropoffValidator(object):
#     def __call__(self, value):
#         dropoff_time = value.get('dropoff_time')
#         dropoff_date = value.get('dropoff_date')
#         manual_dropoff_date = value.get('manual_dropoff_date')

#         if dropoff_time:
#             if not dropoff_date:
#                 raise serializers.ValidationError('Drop off date require')
#             elif dropoff_time.day.value != dropoff_date.weekday():
#                 raise serializers.ValidationError('Date provided does not match dropoff time date')

#             start_datetime = timezone.make_aware(
#                 datetime.combine(dropoff_date, dropoff_time.time_start)
#             )

#             if start_datetime < timezone.now():
#                 raise serializers.ValidationError('Cannot schedule dropoff for past date')

#             if (start_datetime - timezone.now()) > timedelta(weeks=12):
#                 raise serializers.ValidationError('Cannot schedule dropoff more than 12 weeks in future')

#         elif manual_dropoff_date:
#             if dropoff_date:
#                 raise serializers.ValidationError('Cannot provide both manual dropoff date and dropoff date')

#         else:
#             raise serializers.ValidationError('You must select a valid dropoff time')

#     def set_context(self, serializer):
#         self.instance = getattr(serializer, 'instance', None)


# class ItemRequestSerializer(serializers.ModelSerializer):
#     category_tag = serializers.CharField(source='category.tag')
#     category_display_name = serializers.CharField(source='category.display_name')

#     class Meta:
#         model = Item
#         fields = (
#             'id', 'tag', 'display_name', 'category_tag', 'category_display_name'
#         )
#         read_only_fields = (
#             'id', 'tag', 'display_name', 'category_tag', 'category_display_name'
#         )


# class DonationFulfillmentSerializer(serializers.ModelSerializer):
#     code = serializers.CharField(source='request.code', read_only=True)
#     request = serializers.PrimaryKeyRelatedField(
#         queryset=Request.unfulfilled.all()
#     )

#     def validate_accepted(self, value):
#         if not value:
#             raise serializers.ValidationError('You must accept the terms in order to fulfill a request.')
#         return value

#     class Meta:
#         model = DonationFulfillment
#         fields = (
#             'id', 'name', 'phone', 'email', 'request', 'dropoff_time', 'dropoff_date',
#             'manual_dropoff_date', 'created', 'code', 'accepted'
#         )
#         read_only_fields = (
#             'id', 'created',
#         )
#         # TODO: Add validator to raise error when request has already been fulfilled
#         #       (currently raises vague 'object does not exist' error)
#         validators = [ContactInfoValidator(), DropoffValidator()]
#         extra_kwargs = {
#             'accepted': {'required': True},
#             'email': {'required': True},
#         }


class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = (
            'id', 'name',
        )


class RequestSerializer(serializers.ModelSerializer):
    # item = serializers.SlugRelatedField(
    #     slug_field='tag',
    #     queryset=RequestItem.objects.all()
    # )

    def validate_accepted(self, value):
        if not value:
            raise serializers.ValidationError('You must accept the terms in order to submit a request.')
        return value

    class Meta:
        model = Request
        fields = (
            'id',
        )
        extra_kwargs = {
            'accepted': {'required': True},
        }
        read_only_fields = (
            'id', 'created', 'code'
        )
        validators = [ContactInfoValidator()]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('slug', 'display_name')


class RequestItemSerializer(serializers.ModelSerializer):
    type = SubcategorySerializer()

    class Meta:
        model = RequestItem
        fields = ('quantity', 'type')


class RequestPublicSerializer(serializers.ModelSerializer):
    request_items = RequestItemSerializer(many=True)
    neighborhood = NeighborhoodSerializer()

    class Meta:
        model = Request
        fields = (
            'id', 'neighborhood', 'created', 'request_items'
        )


class LocationSerializer(serializers.ModelSerializer):
    neighborhood = NeighborhoodSerializer()
    org = serializers.CharField(source='org.name', read_only=True)

    class Meta:
        model = Location
        fields = (
            'org', 'name', 'neighborhood', 'street_address_1',
            'street_address_2', 'city', 'state', 'zipcode', 'phone', 'website', 'maps_url'
        )


class DatedEventListSerializer(serializers.ListSerializer):
    def to_representation(self, items):
        data = []

        for item in items:
            item_data = self.child.to_representation(item)

            if item.type == ScheduleType.WEEKLY:
                for date in item.get_visible_dates():
                    start_datetime = datetime.combine(date, item.start_time)
                    item_data = self.child.to_representation(item)
                    item_data['date'] = date
                    data.append((start_datetime, item_data))
            elif item.type == ScheduleType.INDIVIDUAL:
                start_datetime = datetime.combine(item.date, item.start_time)
                item_data = self.child.to_representation(item)
                data.append((start_datetime, item_data))

        return [appointment_data for _, appointment_data in sorted(data, key=lambda item: item[0])]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('display_name', 'slug', 'image', 'inline_text_name', 'plural_pronoun')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('display_name', 'slug', 'subcategories')


class DatedEventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    location = LocationSerializer()
    date = serializers.DateField(read_only=True)
    start_time = serializers.TimeField(read_only=True)
    end_time = serializers.TimeField(read_only=True)

    class Meta:
        model = Event
        list_serializer_class = DatedEventListSerializer
        fields = ('id', 'location', 'date', 'start_time', 'end_time')
