from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response

from donations.models import (
    DonationFulfillment, DonationRequest, DropoffTime, Neighborhood
)
from donations.serializers import (
    DonationFulfillmentSerializer, DonationRequestPublicSerializer,
    DonationRequestSerializer, DropoffTimeSerializer, NeighborhoodSerializer
)


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


class DonationFulfillmentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = DonationFulfillment.objects.all()
    serializer_class = DonationFulfillmentSerializer


class DonationRequestCodeDetailView(generics.RetrieveAPIView):
    queryset = DonationRequest.objects.all()
    serializer_class = DonationRequestSerializer
    lookup_field = 'code'


class NeighborhoodViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Neighborhood.objects.all()
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
