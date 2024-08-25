from django.urls import path, include
from rest_framework import routers

from photo_cards.views import PhotoCardSalesViewSet

router = routers.SimpleRouter()
router.register("sales", PhotoCardSalesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]