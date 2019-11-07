from django.contrib import admin

from core.admin import RelatedOrgPermissionModelAdmin
from donations.models import (
    Category, Request,
    # DropoffTime,
    Location,
    # ManualDropoffDate,
    Neighborhood,
    DonorAppointment,
    Event,
    FulfillmentItem,
    Subcategory,
    RequestItem,
    SizeChoice,
    ScheduleType
)
from organizations.models import Org
from suit.admin import SortableModelAdmin, SortableStackedInline


class RequestItemInline(admin.TabularInline):
    model = RequestItem
    fk_name = 'request'


class RelatedOrgListFilter(admin.SimpleListFilter):
    title = 'organization'
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            orgs = Org.objects.all()
        else:
            orgs = request.user.orgs.all()

        return (
            (org.id, org.name) for org in orgs.all()
        )

    def queryset(self, request, queryset):
        org_id = self.value()

        if not org_id:
            return queryset
        else:
            return queryset.filter(org_id=org_id)


class LocationAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'name', 'organization', 'neighborhood'
        ),
        'restricted': (
            'name', 'neighborhood'
        ),
    }

    def organization(self, obj):
        return obj.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('org')

    organization.admin_order_field = 'org__name'


class EventAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'location', 'day_of_week', 'organization', 'type', 'start_time', 'end_time', 'is_public', 'is_cancelled'
        ),
        'restricted': (
            'location', 'day_of_week', 'type', 'start_time', 'end_time', 'is_public', 'is_cancelled'
        )
    }
    list_filter = ('type', 'location', 'is_cancelled', 'day_of_week')

    def organization(self, obj):
        if obj.location:
            return obj.location.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('location__org')

    def changelist_view(self, request, extra_context=None):
        if not request.GET.get('is_cancelled__exact'):
            results = request.GET.copy()
            results['is_cancelled__exact'] = '0'
            request.GET = results
            request.META['QUERY_STRINGS'] = request.GET.urlencode()

        return super().changelist_view(request, extra_context=extra_context)

    organization.admin_order_field = 'location__org__name'


class SubcategoryInline(SortableStackedInline):
    model = Subcategory
    sortable = '_order'
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubcategoryInline]


# class ManualDropoffDateAdmin(RelatedOrgPermissionModelAdmin):
#     pass


# class DonationFulfillmentAdmin(RelatedOrgPermissionModelAdmin):
#     list_filter = (
#         ('dropoff_date', DateRangeFilter),
#     )

#     list_display_choices = {
#         'superuser': (
#             'name', 'organization', 'request'
#         ),
#         'restricted': (
#             'name', 'request'
#         ),
#     }

#     def organization(self, obj):
#         return obj.org

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related(
#             'dropoff_time__location__org'
#         )

#     organization.admin_order_field = 'dropoff_time__location__org__name'


class RequestAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'name', 'neighborhood', 'organization', 'created'
        ),
        'restricted': (
            'name', 'neighborhood', 'created',
        ),
    }

    inlines = [
        RequestItemInline
    ]

    def organization(self, obj):
        return obj.org

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('org')

    list_filter = (
        'name',
        'neighborhood',
        RelatedOrgListFilter,
        'created'
    )

    organization.admin_order_field = 'org__name'


class DonorAppointmentAdmin(RelatedOrgPermissionModelAdmin):
    list_display_choices = {
        'superuser': (
            'request', 'event', 'location', 'quantity', 'date', 'start_time', 'end_time', 'is_cancelled', 'accepted_terms'
        ),
        'restricted': (
            'request', 'event', 'location', 'quantity', 'date', 'start_time', 'end_time', 'is_cancelled', 'accepted_terms'
        ),
    }

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)

        if obj and obj.id:
            return ('request',)
        else:
            return ()


# class SubcategoryAdmin(SortableModelAdmin):
#     list_display = ('display_name', 'category', 'slug')
#     list_filter = ('category', 'slug')
#     sortable = '_order'


admin.site.register(Category, CategoryAdmin)
#admin.site.register(DonationFulfillment, DonationFulfillmentAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Neighborhood)
admin.site.register(DonorAppointment, DonorAppointmentAdmin)
admin.site.register(Event, EventAdmin)
#admin.site.register(FulfillmentItem)
#admin.site.register(Subcategory, SubcategoryAdmin)
#admin.site.register(RequestItem)
admin.site.register(SizeChoice)
#admin.site.register(DropoffTime, DropoffTimeAdmin)
#admin.site.register(ManualDropoffDate, ManualDropoffDateAdmin)
