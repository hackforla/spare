from django.conf.urls import url
from rest_framework import routers

from donations.views import (
    DonationFulfillmentViewSet, DonationRequestCodeDetailView,
    DonationRequestViewSet, NeighborhoodViewSet, LocationViewSet, PickupTimeViewSet
)

router = routers.DefaultRouter()
router.register(r'requests', DonationRequestViewSet, base_name='request')
router.register(r'fulfillments', DonationFulfillmentViewSet, base_name='fulfillments')
router.register(r'neighborhoods', NeighborhoodViewSet, base_name='neighborhoods')
router.register(r'locations', LocationViewSet, base_name='locations')
router.register(r'pickup_times', PickupTimeViewSet, base_name='pickup_times')

urlpatterns = [
    url('^requests/code/(?P<code>[a-zA-Z]+)/$',
        DonationRequestCodeDetailView.as_view(),
        name='request-code-detail')
] + router.urls
