from datetime import datetime, timedelta

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from enumfields import Enum, EnumIntegerField
from phonenumber_field.modelfields import PhoneNumberField

from core.models import (
    AddressModel, RelatedOrgManager, RelatedOrgPermissionModel
)

# Defaults for initial items and categories (used in migrations)
# Each category tuple is mapped to a set (not dict) of tuples containing
# the item tag ('sleeping_bags') and display name ('Sleeping Bags')
DEFAULT_CATEGORIES_AND_ITEMS = {
    ('clothing', 'Clothing'): {
        ('shirts', 'Shirts'),
        ('dresses_skirts', 'Dresses and Skirts'),
        ('hats', 'Hats'),
        ('pants', 'Pants'),
        ('shorts', 'Shorts'),
        ('jacket_sweaters', 'Jackets and Sweaters'),
        ('socks', 'Socks'),
        ('shoes', 'Shoes'),
    },
    ('hygiene', 'Hygiene'): {
        ('toothbrush', 'Toothbrush'),
        ('toothpaste', 'Toothpaste'),
        ('mouthwash', 'Mouthwash'),
        ('soap', 'Soap'),
        ('shampoo_conditioner', 'Shampoo and Conditioner'),
        ('feminine_hygiene', 'Feminine Hygiene'),
    },
    ('essentials', 'Essentials'): {
        ('blankets', 'Blankets'),
        ('sleeping_bags', 'Sleeping Bags'),
        ('cat_food', 'Cat Food'),
        ('dog_food', 'Dog Food'),
    }
}

DEFAULT_NEIGHBORHOODS = [
    'Boyle Heights',
    'Silver Lake',
    'Highland Park',
]


VISIBLE_WEEKS = 2
HOURS_AHEAD = 24


tag_validator = RegexValidator(
    regex='^[a-z_]*$',
    message='Only lower case letters and underscores allowed for tag',
    code='invalid_tag'
)


class ContactModelMixin(models.Model):
    name = models.CharField(max_length=120)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=16, blank=True)

    class Meta:
        abstract = True


class TimestampedModelMixin(models.Model):
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TaggedModelMixin(models.Model):
    tag = models.CharField(
        max_length=120,
        unique=True,
        validators=[tag_validator]
    )
    display_name = models.CharField(max_length=120)

    def __str__(self):
        return str(self.display_name)

    class Meta:
        abstract = True


class Category(TaggedModelMixin, models.Model):
    class Meta:
        verbose_name_plural = 'categories'


class Item(TaggedModelMixin, models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Neighborhood(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Location(RelatedOrgPermissionModel, AddressModel):
    location_name = models.CharField(max_length=100, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='locations')
    maps_url = models.URLField(max_length=160, blank=True)
    notes = models.TextField(blank=True)

    org = models.ForeignKey(
        'organizations.Org',
        on_delete=models.CASCADE,
        related_name='locations'
    )

    def __str__(self):
        return self.location_name


class DaysOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class DropoffTime(RelatedOrgPermissionModel):
    time_start = models.TimeField()
    time_end = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_times')
    day = EnumIntegerField(DaysOfWeek, default=DaysOfWeek.SUNDAY)

    org_lookup = 'location__org'

    def get_visible_dates(self):
        results = []

        now = timezone.now()

        # Get number of days differences to next date
        days_ahead = self.day.value - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        # Get the nearest valid date, given day and start time
        nearest_date = now.date() + timedelta(days=days_ahead)

        # We want to check the start time (plus an additional range of 1 day/24 hours)
        nearest_date_start_time = (
            datetime.combine(nearest_date, self.time_start) + timedelta(hours=HOURS_AHEAD)
        )

        # If that datetime has passed, start with the next week's date
        if timezone.make_aware(nearest_date_start_time) < now:
            nearest_date = nearest_date + timedelta(days=7)

        # Get a date for each visible week
        for weeks in range(VISIBLE_WEEKS):
            results.append(nearest_date + timedelta(days=7 * weeks))

        return results

    def get_related_org(self):
        if self.location:
            return self.location.org

    def __str__(self):
        return '{} - {}'.format(self.location, self.time_start)


class VisibleManualDropoffDates(RelatedOrgManager):
    def get_queryset(self):
        visibility_start = timezone.now() + timedelta(hours=24)
        visibility_end = timezone.now() + timedelta(days=15)

        return super().get_queryset().filter(
            dropoff_date__gte=visibility_start.date(),
            dropoff_date__lte=visibility_end.date(),
        )


class ManualDropoffDate(RelatedOrgPermissionModel):
    time_start = models.TimeField()
    time_end = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='manual_dropoff_dates')
    dropoff_date = models.DateField(null=True)

    objects = RelatedOrgManager()
    visible = VisibleManualDropoffDates()

    org_lookup = 'location__org'

    @property
    def org(self):
        if self.location:
            return self.location.org

    def __str__(self):
        return '{} - {}: {}'.format(self.location, self.dropoff_date, self.time_start)


class UnfulfilledRequestManager(RelatedOrgManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            fulfillments__isnull=True
        )


class ActiveRequestManager(RelatedOrgManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            created__gte=timezone.now() - timedelta(days=10),
            fulfillments__isnull=True
        )


class DonationRequest(RelatedOrgPermissionModel, ContactModelMixin, TimestampedModelMixin):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=16, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    accepted = models.BooleanField(default=False)

    org = models.ForeignKey(
        'organizations.Org',
        on_delete=models.SET_NULL,
        related_name='donation_requests',
        null=True,
        blank=True)

    objects = RelatedOrgManager()
    unfulfilled = UnfulfilledRequestManager()
    active = ActiveRequestManager()

    def __str__(self):
        return '{} - {}'.format(self.item, self.created)


class DonationFulfillment(ContactModelMixin, TimestampedModelMixin, RelatedOrgPermissionModel):
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='fulfillments')
    dropoff_time = models.ForeignKey(DropoffTime, on_delete=models.CASCADE, null=True, blank=True)
    manual_dropoff_date = models.ForeignKey(ManualDropoffDate, on_delete=models.CASCADE, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    dropoff_date = models.DateField(null=True, blank=True)

    org_lookup = 'dropoff_time__location__org'

    @property
    def org(self):
        try:
            return self.dropoff_time.location.org
        except AttributeError:
            return None

    def __str__(self):
        return '{} ({}) - {}'.format(self.request.item, self.location, self.dropoff_date)

    def get_attribute(self, attr):
        if self.dropoff_time:
            return getattr(self.dropoff_time, attr)
        elif self.manual_dropoff_date:
            return getattr(self.manual_dropoff_date, attr)

    @property
    def location(self):
        return self.get_attribute('location')

    @property
    def time_start(self):
        return self.get_attribute('time_start')

    @property
    def time_end(self):
        return self.get_attribute('time_end')

    @property
    def date(self):
        if self.dropoff_time:
            return self.dropoff_date
        elif self.manual_dropoff_date:
            return self.manual_dropoff_date.dropoff_date
