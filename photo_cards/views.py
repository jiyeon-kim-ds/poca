from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from photo_cards.models import PhotoCard, RegisteredPhotoCard
from photo_cards.serializers import PhotoCardSalesSerializer


class PhotoCardSalesViewSet(viewsets.ModelViewSet):
    queryset = RegisteredPhotoCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCardSalesSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(seller_id=self.request.user.id)
        return queryset
    
