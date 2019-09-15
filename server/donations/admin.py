from date_range_filter import DateRangeFilter
from django.contrib import admin

from core.admin import RelatedOrgPermissionModelAdmin
from donations.models import (
    Category, DonationFulfillment, DonationRequest, DropoffTime, Item,
    Location, ManualDropoffDate, Neighborhood
)


class LocationAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'location_name', 'organization', 'neighborhood'
        ),
        'restricted': (
            'location_name', 'neighborhood'
        ),
    }

    def organization(self, obj):
        return obj.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('org')

    organization.admin_order_field = 'org__name'


class ManualDropoffDateAdmin(RelatedOrgPermissionModelAdmin):
    pass


class DonationFulfillmentAdmin(RelatedOrgPermissionModelAdmin):
    list_filter = (
        ('dropoff_date', DateRangeFilter),
    )

    list_display_choices = {
        'superuser': (
            'name', 'organization', 'request'
        ),
        'restricted': (
            'name', 'request'
        ),
    }

    def organization(self, obj):
        return obj.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'dropoff_time__location__org'
        )

    organization.admin_order_field = 'dropoff_time__location__org__name'


class DonationRequestAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'item', 'neighborhood', 'organization', 'created'
        ),
        'restricted': (
            'item', 'neighborhood', 'created',
        ),
    }

    def organization(self, obj):
        return obj.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('org')

    organization.admin_order_field = 'org__name'


class DropoffTimeAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'location', 'organization', 'neighborhood', 'time_start', 'time_end'
        ),
        'restricted': (
            'location', 'neighborhood', 'time_start', 'time_end'
        ),
    }

    def neighborhood(self, obj):
        return obj.location.neighborhood

    def organization(self, obj):
        return obj.location.org

    neighborhood.admin_order_field = 'location__neighborhood__name'
    organization.admin_order_field = 'location__org__name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related(
            'location', 'location__neighborhood', 'location__org')

        return queryset

    ordering = ('location__neighborhood__name', 'time_start')


admin.site.register(Category)
admin.site.register(DonationFulfillment, DonationFulfillmentAdmin)
admin.site.register(DonationRequest, DonationRequestAdmin)
admin.site.register(Item)
admin.site.register(Location, LocationAdmin)
admin.site.register(Neighborhood)
admin.site.register(DropoffTime, DropoffTimeAdmin)
admin.site.register(ManualDropoffDate, ManualDropoffDateAdmin)
