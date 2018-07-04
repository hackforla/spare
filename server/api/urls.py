from django.conf.urls import url
from rest_framework import routers

from donations.views import (
    DonationFulfillmentViewSet, DonationRequestCodeDetailView,
    DonationRequestViewSet, NeighborhoodViewSet, DropoffTimeListView
)

router = routers.DefaultRouter()
router.register(r'requests', DonationRequestViewSet, base_name='request')
router.register(r'fulfillments', DonationFulfillmentViewSet, base_name='fulfillments')
router.register(r'neighborhoods', NeighborhoodViewSet, base_name='neighborhoods')

urlpatterns = [
    url('^requests/code/(?P<code>[a-zA-Z]+)/$',
        DonationRequestCodeDetailView.as_view(),
        name='request-code-detail'),
    url('^requests/(?P<request_id>[a-z0-9]+)/dropoff_times/$',
        DropoffTimeListView.as_view(),
        name='request-dropoff-times-list'),
] + router.urls
