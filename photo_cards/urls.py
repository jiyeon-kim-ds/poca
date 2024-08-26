from django.urls import path, include
from rest_framework import routers

from photo_cards.views import PhotoCardSalesViewSet, PhotoCardPurchaseViewSet

router = routers.SimpleRouter()
router.register("sales", PhotoCardSalesViewSet, basename="registered_photo_cards")
router.register("available", PhotoCardPurchaseViewSet, basename="available_photo_cards")

urlpatterns = [
    path("", include(router.urls)),
]