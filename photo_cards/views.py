from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Min, Max
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404

from photo_cards.models import RegisteredPhotoCard
from photo_cards.serializers import (
    PhotoCardSalesSerializer,
    RegisteredPhotoCardListSerializer,
    RegisteredPhotoCardDetailSerializer,
)


class PhotoCardSalesViewSet(viewsets.ModelViewSet):
    queryset = RegisteredPhotoCard.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoCardSalesSerializer
    http_method_names = ["post"]

    def get_queryset(self):
        queryset = self.queryset.filter(seller_id=self.request.user.id)
        return queryset


class PhotoCardPurchaseViewSet(viewsets.ModelViewSet):
    queryset = RegisteredPhotoCard.objects.all()
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        method = self.request.method

        if method == "GET":
            if self.action == "list":
                # 전체 목록 조회
                return self.queryset.filter(state="available")
            else:
                return self.queryset.filter(id=self.kwargs["pk"])
        else:
            # 구매(PARTIAL_UPDATE) 요청
            obj_id = self.kwargs.get('pk')
            return self.queryset.filter(id=obj_id)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return RegisteredPhotoCardListSerializer
        elif self.action == "retrieve":
            return RegisteredPhotoCardDetailSerializer

    def list(self, request):
        queryset = self.get_queryset()

        # 최저가 포토카드 서브쿼리
        min_price_subquery = queryset.filter(
            photo_card_id=OuterRef("photo_card_id")
        ).values("photo_card_id").annotate(
            min_price=Min("price")
        ).values("min_price")

        # 최신 수정 포토카드 서브쿼리
        latest_renewal_subquery = queryset.filter(
            photo_card_id=OuterRef("photo_card_id"),
            price=OuterRef("price")
        ).values("photo_card_id").annotate(
            latest_renewal=Max("renewal_date")
        ).values("latest_renewal")

        filtered_queryset = queryset.annotate(
            min_price=Subquery(min_price_subquery)
        ).filter(
            price=F("min_price")
        ).annotate(
            latest_renewal=Subquery(latest_renewal_subquery)
        ).filter(
            renewal_date=F("latest_renewal")
        )

        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)