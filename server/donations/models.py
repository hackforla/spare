from datetime import date, datetime, timedelta

from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from enumfields import Enum, EnumIntegerField
from phonenumber_field.modelfields import PhoneNumberField

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


zipcode_validator = RegexValidator(
    message='Invalid zip code format (must be 5 or 9 digits)',
    code='invalid_zipcode',
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


class Location(models.Model):
    location_name = models.CharField(max_length=100, blank=True)
    organization_name = models.CharField(max_length=100, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='locations')
    street_address_1 = models.CharField(max_length=150)
    street_address_2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=50, default='Los Angeles')
    state = models.CharField(max_length=2, default='CA')
    zipcode = models.CharField(max_length=10, validators=[zipcode_validator], default='90042')
    phone = models.CharField(max_length=10, blank=True)
    website = models.URLField(max_length=100, blank=True)
    maps_url = models.URLField(max_length=160, blank=True)
    notes = models.TextField(blank=True)

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


class DropoffTime(models.Model):
    time_start = models.TimeField()
    time_end = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='dropoff_times')
    day = EnumIntegerField(DaysOfWeek, default=DaysOfWeek.SUNDAY)

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

    def __str__(self):
        return '{} - {}'.format(self.location, self.time_start)


class VisibleManualDropoffDates(models.Manager):
    def get_queryset(self):
        visibility_start = timezone.now() + timedelta(hours=24)
        visibility_end = timezone.now() + timedelta(days=15)

        return super().get_queryset().filter(
            dropoff_date__gte=visibility_start.date(),
            dropoff_date__lte=visibility_end.date(),
        )


class ManualDropoffDate(models.Model):
    time_start = models.TimeField()
    time_end = models.TimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='manual_dropoff_dates')
    dropoff_date = models.DateField(null=True)

    objects = models.Manager()
    visible = VisibleManualDropoffDates()

    def __str__(self):
        return '{} - {}'.format(self.location, self.time_start)


class UnfulfilledRequestManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            fulfillments__isnull=True
        )


class ActiveRequestManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            created__gte=timezone.now() - timedelta(days=10),
            fulfillments__isnull=True
        )


class DonationRequest(ContactModelMixin, TimestampedModelMixin, models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    size = models.CharField(max_length=16, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)

    objects = models.Manager()
    unfulfilled = UnfulfilledRequestManager()
    active = ActiveRequestManager()

    def __str__(self):
        return '{} - {}'.format(self.item, self.created)


class DonationFulfillment(ContactModelMixin, TimestampedModelMixin, models.Model):
    request = models.ForeignKey(DonationRequest, on_delete=models.CASCADE, related_name='fulfillments')
    dropoff_time = models.ForeignKey(DropoffTime, on_delete=models.CASCADE)
    dropoff_date = models.DateField(null=True)

    def __str__(self):
        return '{} - {}'.format(self.request.item, self.created)
