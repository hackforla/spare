from django.contrib import admin

from donations.models import (
    Category, DonationFulfillment, DonationRequest, DropoffTime, Item,
    Location, Neighborhood
)

admin.site.register(Category)
admin.site.register(DonationFulfillment)
admin.site.register(DonationRequest)
admin.site.register(Item)
admin.site.register(Location)
admin.site.register(Neighborhood)
admin.site.register(DropoffTime)
