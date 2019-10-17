from unittest.mock import Mock

import pytest
from rest_framework.test import APIClient

from core.models import User
from donations.models import (
    DaysOfWeek, DonationFulfillment, DonationRequest, DropoffTime, Item,
    Location, Neighborhood
)
from organizations.models import Org, OrgUserRole, OrgUserRoleType


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def shirts():
    return Item.objects.get(tag='shirts')


@pytest.fixture
def neighborhood():
    return Neighborhood.objects.first()


@pytest.fixture
def donation_request(shirts, neighborhood):
    return DonationRequest.objects.create(
        name='Jimbo',
        phone='+5556667777',
        email='jimbojones@example.com',
        city='Los Angeles',
        item=shirts,
        size='L',
        neighborhood=neighborhood
    )


@pytest.fixture
def org():
    org = Org.objects.create(
        name='Test Org',
        email='org_owner@example.com',
        ein='111222333',
        street_address_1='456 Fake Ave',
        city='Los Angeles',
        state='CA',
        phone='5550000000',
        zipcode='90100',
    )

    return org


@pytest.fixture
def org_user(org):
    org_user = User.objects.create(
        email='org_user@example.com',
        display_name='Org User',
        is_staff=True,
        is_superuser=False
    )
    OrgUserRole(
        type=OrgUserRoleType.ADMIN,
        user=org_user,
        org=org,
    )

    return org_user


@pytest.fixture
def location(neighborhood, org):
    return Location.objects.create(
        location_name='LA Coffee',
        org=org,
        neighborhood=neighborhood,
        street_address_1='123 Fake St',
        city='Los Angeles',
        state='CA',
        zipcode='90100',
        phone='5550000000',
    )


@pytest.fixture
def dropoff_time(location):
    return DropoffTime.objects.create(
        time_start='11:00:00',
        time_end='12:00:00',
        location=location,
        day=DaysOfWeek.MONDAY,
    )


@pytest.fixture
def donation_fulfillment(dropoff_time, shirts, neighborhood):
    donation_request = DonationRequest.objects.create(
        name='Nelson',
        phone='+5554443333',
        email='nelsonmuntz@example.com',
        city='Los Angeles',
        item=shirts,
        size='XL',
        neighborhood=neighborhood
    )

    return DonationFulfillment.objects.create(
        name='Lisa',
        phone='+5553337777',
        email='lsimpson@example.com',
        city='Los Angeles',
        request=donation_request,
        dropoff_time=dropoff_time,
    )


@pytest.fixture(autouse=True)
def smsoutbox():
    from core import sms
    sms.outbox = []

    return sms.outbox
