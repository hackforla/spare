import os
from datetime import datetime, timedelta

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone

from core.models import (
    AddressModel, OrderedModel, RelatedOrgManager, RelatedOrgPermissionModel,
    ContactModel, TimestampedModel
)
from enumfields import Enum, EnumField, EnumIntegerField

# Arbitrary static date (for easily comparing time range values)
REFERENCE_DATE = datetime(1, 1, 1, 0, 0)

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


class Category(models.Model):
    display_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=32, unique=True)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name_plural = 'categories'


def get_subcategory_upload_to(instance, filename):
    # Get extension
    _, ext = os.path.splitext(filename)
    return 'categories/{slug}{ext}'.format(
        slug=instance.slug,
        ext=ext
    )


class SizeCategory(Enum):
    MENS = 'mens'
    WOMENS = 'womens'
    UNISEX = 'adult-unisex'
    YOUTH = 'youth'
    BOYS = 'boys'
    GIRLS = 'girls'
    INFANTS = 'infants'
    TODDLER = 'toddlers'


class SizeChoice(models.Model):
    choice_data = JSONField()
    category = EnumField(SizeCategory, max_length=32, blank=True)

    def __str__(self):
        return "Size choice #{}".format(self.id)


class Subcategory(OrderedModel):
    display_name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=32, unique=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories')

    image = models.ImageField(
        upload_to=get_subcategory_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    # Copy-related fields
    inline_text_name = models.CharField(max_length=64)
    plural_pronoun = models.BooleanField()

    # Sizes
    size_choices = models.ManyToManyField(SizeChoice, related_name='subcategories', blank=True)

    def __str__(self):
        return self.display_name

    def get_ordering_queryset(self):
        return self.category.item_types.all()

    class Meta:
        verbose_name_plural = 'subcategories'


class Neighborhood(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Location(RelatedOrgPermissionModel, AddressModel):
    name = models.CharField(max_length=100, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='locations')
    maps_url = models.URLField(max_length=160, blank=True)
    notes = models.TextField(blank=True)

    org = models.ForeignKey(
        'organizations.Org',
        on_delete=models.CASCADE,
        related_name='locations'
    )

    def __str__(self):
        return self.name


class DaysOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class UnfulfilledRequestManager(RelatedOrgManager):
    pass
    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         # fulfillments__isnull=True
    #     )


class ActiveRequestManager(RelatedOrgManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            created__gte=timezone.now() - timedelta(days=10),
            # fulfillments__isnull=True
        )


class RequestItem(RelatedOrgPermissionModel):
    type = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='request_items')
    quantity = models.PositiveIntegerField(default=1)
    request = models.ForeignKey('Request', on_delete=models.PROTECT, related_name='request_items')

    org__lookup = 'request__location__org'


    def __str__(self):
        return self.type.__str__()


    def get_related_org(self):
        if self.location:
            return self.location.org


class ScheduleType(Enum):
    WEEKLY = 'w'
    ONE_OFF = 'i'

    class Labels:
        ONE_OFF = 'One-Off'


class EventsManager(RelatedOrgManager):
    def public(self):
        return self.get_queryset().filter(
            is_public=True
        )


class Event(RelatedOrgPermissionModel):
    """
    Scheduled or ad-hoc events
    """
    type = EnumField(ScheduleType, default=ScheduleType.WEEKLY, max_length=1)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True)
    day_of_week = EnumIntegerField(DaysOfWeek, blank=True, null=True)
    is_cancelled = models.BooleanField(default=False, editable=False)
    is_public = models.BooleanField(default=True)

    # Required if individual schedule type (otherwise invalid)
    date = models.DateField(blank=True, null=True)

    objects = EventsManager()

    org_lookup = 'location__org'

    def get_visible_dates(self):
        results = []

        now = timezone.now()

        # Get number of days differences to next date
        days_ahead = self.day_of_week.value - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7

        # Get the nearest valid date, given day and start time
        nearest_date = now.date() + timedelta(days=days_ahead)

        # We want to check the start time (plus an additional range of 1 day/24 hours)
        nearest_date_start_time = (
            datetime.combine(nearest_date, self.start_time) + timedelta(hours=HOURS_AHEAD)
        )

        # If that datetime has passed, start with the next week's date
        if timezone.make_aware(nearest_date_start_time) < now:
            nearest_date = nearest_date + timedelta(days=7)

        # Get a date for each visible week
        for weeks in range(VISIBLE_WEEKS):
            results.append(nearest_date + timedelta(days=7 * weeks))

        return results

    def _get_date_validation_error(self):
        error = {}

        if (self.type == ScheduleType.WEEKLY) and self.date is not None:
            error['date'] = 'Cannot specify date for recurring appointments'
        elif (self.type == ScheduleType.ONE_OFF) and self.date is None:
            error['date'] = 'Date required for individual appointments'

        return error

    def _get_time_range_validation_error(self):
        error = {}
        start_time = datetime.combine(REFERENCE_DATE, self.start_time)
        end_time = datetime.combine(REFERENCE_DATE, self.end_time)
        delta = end_time - start_time

        if delta < timedelta(minutes=15):
            error['end_time'] = 'Invalid end time. Events must be at least 15 minutes in length.'
        elif delta > timedelta(hours=6):
            error['end_time'] = 'Invalid end time. Events cannot exceed 6 hours.'

        return error

    def __str__(self):
        # TODO: Full formatting of appointment name
        return 'Event #{}'.format(self.id)

    def clean(self):
        errors = {}

        # If no end time was provided, default to 15 minutes
        if self.start_time and not self.end_time:
            start_time = datetime.combine(REFERENCE_DATE, self.start_time)
            end_time = start_time + timedelta(minutes=15)
            self.end_time = end_time.time()

        elif not (self.start_time and self.end_time):
            return

        errors.update(self._get_date_validation_error())
        errors.update(self._get_time_range_validation_error())

        if errors:
            raise ValidationError(errors)

    def get_related_org(self):
        if self.location:
            return self.location.org


class Request(RelatedOrgPermissionModel, ContactModel, TimestampedModel):
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT)
    accepted_terms = models.BooleanField(default=False, editable=False)
    accepted_terms_date = models.DateTimeField(auto_now=True, editable=False)
    valid_events = models.ManyToManyField(Event, blank=True, related_name='requests')
    is_ongoing = models.BooleanField(default=False)

    org = models.ForeignKey(
        'organizations.Org',
        on_delete=models.SET_NULL,
        related_name='donation_requests',
        null=True,
        blank=True)

    unfulfilled = UnfulfilledRequestManager()
    active = ActiveRequestManager()

    def __str__(self):
        return 'Request #{}'.format(self.id)


class FulfillmentItem(RelatedOrgPermissionModel):
    request_item = models.ForeignKey(RequestItem, on_delete=models.PROTECT, related_name='fulfillment_items')
    quantity = models.PositiveIntegerField(default=1)
    appointment = models.ForeignKey('DonorAppointment', related_name='fulfillment_items')

    class Meta:
        unique_together = ('request_item', 'appointment')


class Fulfillment(RelatedOrgPermissionModel, ContactModel, TimestampedModel, OrderedModel):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='fulfillments')
    fulfillment_items = models.ManyToManyField(FulfillmentItem, related_name='fulfillments')


class DonorAppointment(RelatedOrgPermissionModel, TimestampedModel):
    fulfillment = models.ForeignKey(Fulfillment, on_delete=models.CASCADE, related_name='donor_appointments')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='appointments')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='appointments')
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_cancelled = models.BooleanField(default=False)
    accepted_terms = models.BooleanField(default=False)
    accepted_terms_date = models.DateTimeField(auto_now=True)

    org_lookup = 'donor_appointment__location__org'

    @property
    def org(self):
        try:
            return self.location.org
        except AttributeError:
            return None

    def __str__(self):
        return self.date.__str__()
