from django.contrib import admin
from rangefilter.filter import DateRangeFilter

from donations.models import (
    Category, DonationFulfillment, DonationRequest, DropoffTime, Item,
    Location, ManualDropoffDate, Neighborhood
)


class DonationFulfillmentAdmin(admin.ModelAdmin):
    list_filter = (
        ('dropoff_date', DateRangeFilter),
    )


class DropoffTimeAdmin(admin.ModelAdmin):
    list_display = ('location', 'neighborhood', 'time_start', 'time_end')

    def neighborhood(self, obj):
        return obj.location.neighborhood

    neighborhood.admin_order_field = 'location__neighborhood__name'

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related(
            'location', 'location__neighborhood')

        return queryset

    ordering = ('location__neighborhood__name', 'time_start')


admin.site.register(Category)
admin.site.register(DonationFulfillment, DonationFulfillmentAdmin)
admin.site.register(DonationRequest)
admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Neighborhood)
admin.site.register(DropoffTime, DropoffTimeAdmin)
admin.site.register(ManualDropoffDate)
