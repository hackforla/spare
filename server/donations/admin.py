from django.contrib import admin

from donations.models import (
    Category, DonationFulfillment, DonationRequest, DropoffTime, Item,
    Location, ManualDropoffDate, Neighborhood
)

from rangefilter.filter import DateRangeFilter

class DonationFulfillmentAdmin(admin.ModelAdmin):
    #list_filter = (DropoffDateFilter,)
    list_filter = (
        ('dropoff_date', DateRangeFilter),
    )

admin.site.register(Category)
admin.site.register(DonationFulfillment, DonationFulfillmentAdmin)
admin.site.register(DonationRequest)
admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Neighborhood)
admin.site.register(DropoffTime)
admin.site.register(ManualDropoffDate)
