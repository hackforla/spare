from rest_framework import routers

from donations.views import DonationFulfillmentViewSet, DonationRequestViewSet

router = routers.DefaultRouter()
router.register(r'requests', DonationRequestViewSet, base_name='request')
router.register(r'fulfillments', DonationFulfillmentViewSet, base_name='fulfillments')

urlpatterns = router.urls
