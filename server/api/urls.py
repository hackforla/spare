from django.conf.urls import url
from rest_framework import routers

from donations.views import (
    # DonationFulfillmentViewSet,
    RequestViewSet,
    EventListView,
    NeighborhoodViewSet,
    CategoryViewSet
)

router = routers.DefaultRouter()
router.register(r'requests', RequestViewSet, base_name='request')
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'neighborhoods', NeighborhoodViewSet, base_name='neighborhood')

urlpatterns = router.urls

urlpatterns = [
    url('^requests/(?P<request_id>[a-z0-9]+)/events/$',
        EventListView.as_view(),
        name='request-available-events-list'),
] + router.urls
