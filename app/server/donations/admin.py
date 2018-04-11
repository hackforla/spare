from django.contrib import admin

from donations.models import Category, Subcategory, DonationRequest

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(DonationRequest)
