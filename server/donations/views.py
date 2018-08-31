from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from core.utils import is_test_email, is_test_phone
from donations.models import (
    DonationFulfillment, DonationRequest, DropoffTime, Neighborhood
)
from donations.serializers import (
    DonationFulfillmentSerializer, DonationRequestPublicSerializer,
    DonationRequestSerializer, DropoffTimeSerializer, NeighborhoodSerializer
)


class DonationRequestThrottle(UserRateThrottle):
    rate = '12/day'

    def get_cache_key(self, request, view):
        # Ignore test emails/phone when throttling
        email = request.data.get('email')
        phone = request.data.get('phone')

        if email and is_test_email(email):
            return None

        if phone and is_test_phone(phone):
            return None

        # Otherwise, regular throttling
        else:
            return super().get_cache_key(request, view)


class DonationRequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # Limit to unfulfilled requests made within last 10 days
    def get_queryset(self):
        queryset = DonationRequest.active.all()
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood is not None:
            queryset = queryset.filter(neighborhood=neighborhood)

        return queryset

    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('item__category__tag', 'item__tag',)

    def get_serializer_class(self):
        if self.action == 'create':
            return DonationRequestSerializer
        else:
            return DonationRequestPublicSerializer

    def get_throttles(self):
        if self.request.method == 'GET':
            return []
        else:
            return [DonationRequestThrottle()]


class DonationFulfillmentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DonationFulfillment.objects.all()
    serializer_class = DonationFulfillmentSerializer

    def get_throttles(self):
        if self.request.method == 'GET':
            return []
        else:
            return [DonationRequestThrottle()]


class DonationRequestCodeDetailView(generics.RetrieveAPIView):
    # NOTE: This view is currently not being used, but potentially planned for future
    #       use
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    lookup_field = 'code'


class NeighborhoodViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # Only show neighborhoods with at least one dropoff time
    queryset = Neighborhood.objects.filter(
        locations__dropoff_times__isnull=False
    )
    serializer_class = NeighborhoodSerializer


class DropoffTimeListView(generics.GenericAPIView):
    def get_queryset(self):
        return DropoffTime.objects.all()

    def get(self, request, request_id):
        request_obj = get_object_or_404(DonationRequest, id=request_id)

        # TODO: Allow selection from nearby neighborhoods
        neighborhood = request_obj.neighborhood
        dropoff_times = DropoffTime.objects.filter(location__neighborhood=neighborhood)

        serializer = DropoffTimeSerializer(dropoff_times, many=True)
        return Response(serializer.data)
