from django.contrib import admin

from donations.models import (
    Category, DonationFulfillment, DonationRequest, Item
)

admin.site.register(Category)
admin.site.register(DonationFulfillment)
admin.site.register(DonationRequest)
admin.site.register(Item)
