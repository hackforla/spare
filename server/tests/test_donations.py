from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from donations.models import DonationFulfillment


def get_closest_matching_dropoff_date(date, dropoff_time):
    days_difference = date.weekday() - dropoff_time.day.value

    return date - timedelta(days=days_difference)


@pytest.mark.django_db
def test_donation_valid_dropoff_date(client, donation_request, dropoff_time):
    future_date = timezone.now().date() + timedelta(weeks=8)
    valid_date = get_closest_matching_dropoff_date(future_date, dropoff_time)

    assert not DonationFulfillment.objects.exists()

    data = {
        'email': 'demouser@example.com',
        'request': donation_request.id,
        'dropoff_time': dropoff_time.id,
        'dropoff_date': valid_date.isoformat()
    }

    response = client.post(
        reverse('fulfillments-list'),
        data
    )

    fulfillment = DonationFulfillment.objects.get()

    assert response.status_code == status.HTTP_201_CREATED
    assert fulfillment.id == response.data['id']


@pytest.mark.django_db
def test_donation_invalid_past_dropoff_date(client, donation_request, dropoff_time):
    past_date = timezone.now().date() - timedelta(weeks=8)
    valid_date = get_closest_matching_dropoff_date(past_date, dropoff_time)

    assert not DonationFulfillment.objects.exists()

    data = {
        'email': 'demouser@example.com',
        'request': donation_request.id,
        'dropoff_time': dropoff_time.id,
        'dropoff_date': valid_date.isoformat()
    }

    response = client.post(
        reverse('fulfillments-list'),
        data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not DonationFulfillment.objects.exists()


@pytest.mark.django_db
def test_donation_invalid_future_dropoff_date(client, donation_request, dropoff_time):
    future_date = timezone.now().date() + timedelta(weeks=52)
    valid_date = get_closest_matching_dropoff_date(future_date, dropoff_time)

    assert not DonationFulfillment.objects.exists()

    data = {
        'email': 'demouser@example.com',
        'request': donation_request.id,
        'dropoff_time': dropoff_time.id,
        'dropoff_date': valid_date.isoformat()
    }

    response = client.post(
        reverse('fulfillments-list'),
        data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not DonationFulfillment.objects.exists()


@pytest.mark.django_db
def test_donation_invalid_mismatch_dropoff_date(client, donation_request, dropoff_time):
    future_date = timezone.now().date() + timedelta(weeks=8)
    valid_date = get_closest_matching_dropoff_date(future_date, dropoff_time)
    invalid_date = valid_date + timedelta(days=1)

    assert not DonationFulfillment.objects.exists()

    data = {
        'email': 'demouser@example.com',
        'request': donation_request.id,
        'dropoff_time': dropoff_time.id,
        'dropoff_date': invalid_date.isoformat()
    }

    response = client.post(
        reverse('fulfillments-list'),
        data
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert not DonationFulfillment.objects.exists()

    data['dropoff_date'] = valid_date

    response = client.post(
        reverse('fulfillments-list'),
        data
    )

    fulfillment = DonationFulfillment.objects.get()

    assert response.status_code == status.HTTP_201_CREATED
    assert fulfillment.id == response.data['id']
