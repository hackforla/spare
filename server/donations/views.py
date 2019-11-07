from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from core.utils import is_test_email, is_test_phone
from donations.models import (
    Request,
    Event,
    Neighborhood,
    Category
)
from donations.serializers import (
    RequestPublicSerializer,
    RequestSerializer,
    DatedEventSerializer,
    NeighborhoodSerializer,
    CategorySerializer
)


class RequestThrottle(UserRateThrottle):
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


class RequestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    # Limit to unfulfilled requests made within last 10 days
    def get_queryset(self):
        queryset = Request.active.all()
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood is not None:
            queryset = queryset.filter(neighborhood=neighborhood)

        return queryset

    filter_backends = (DjangoFilterBackend,)
    #filter_fields = ('request__items__item_type__category__slug, request__items__item_type__slug',)

    def get_serializer_class(self):
        if self.action == 'create':
            return RequestSerializer
        else:
            return RequestPublicSerializer

    def get_throttles(self):
        if self.request.method == 'GET':
            return []
        else:
            return [RequestThrottle()]


# class DonationFulfillmentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     queryset = DonationFulfillment.objects.all()
#     serializer_class = DonationFulfillmentSerializer

#     def get_throttles(self):
#         if self.request.method == 'GET':
#             return []
#         else:
#             return [RequestThrottle()]'

class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class NeighborhoodViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    # TODO: Only show neighborhoods with at least one dropoff time
    queryset = Neighborhood.objects.all()
    serializer_class = NeighborhoodSerializer


class EventListView(generics.GenericAPIView):
    queryset = Event.objects.public()

    def get(self, request, request_id):
        request_obj = get_object_or_404(Request, id=request_id)

        # If restricted to specific appointment times, return
        # these values
        valid_events = request_obj.valid_events.filter(
            #is_public=True
        )

        if not valid_events:
            neighborhood = request_obj.neighborhood
            valid_events = Event.objects.public().filter(location__neighborhood=neighborhood)

        serializer = DatedEventSerializer(valid_events.all(), many=True)

        return Response(serializer.data)
