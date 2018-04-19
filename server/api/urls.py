from django.conf.urls import url
from rest_framework import routers

from donations.views import (
    DonationFulfillmentViewSet, DonationRequestCodeDetailView,
    DonationRequestViewSet
)

router = routers.DefaultRouter()
router.register(r'requests', DonationRequestViewSet, base_name='request')
router.register(r'fulfillments', DonationFulfillmentViewSet, base_name='fulfillments')

urlpatterns = [
    url('^requests/code/(?P<code>[a-zA-Z]+)/$',
        DonationRequestCodeDetailView.as_view(),
        name='request-code-detail')
] + router.urls
