import logging

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.models import F, Min, Max
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404

from photo_cards.models import RegisteredPhotoCard
from photo_cards.serializers import (
    PhotoCardSalesSerializer,
    RegisteredPhotoCardListSerializer,
    RegisteredPhotoCardDetailSerializer,
    RegisteredPhotoCardUpdateSerializer,
)


logger = logging.getLogger(__name__)

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
                # 전체 목록 조회(LIST
                return self.queryset.filter(state=RegisteredPhotoCard.AVAILABLE)
            else:
                # 객체 상제 조회(RETRIEVE)
                return self.queryset
        else:
            # 구매(PARTIAL_UPDATE) 요청
            obj_id = self.kwargs.get('pk')
            return self.queryset.filter(id=obj_id)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return RegisteredPhotoCardListSerializer
        elif self.action == "retrieve":
            return RegisteredPhotoCardDetailSerializer
        elif self.action == "partial_update":
            return RegisteredPhotoCardUpdateSerializer

    def get_permissions(self):
        if self.action == "partial_update":
            permission_classes = [IsAuthenticated()]
        else:
            permission_classes = []
        return [permission for permission in permission_classes]

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
    
    def get_cheapest_card(self, obj):
        try:
            cheapest_obj = self.queryset.filter(
                photo_card_id=obj.photo_card.id,
                state=RegisteredPhotoCard.AVAILABLE
            ).order_by("price", "renewal_date")[0]

            return cheapest_obj
        except Exception as e:
            logger.error(
                f"에러가 발생했습니다: {str(e)}, \
URL: {self.request.path}"
                )
            raise NotFound("구매 가능한 상품이 아닙니다.")

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        cheapest_obj = self.get_cheapest_card(instance)

        if cheapest_obj != instance:
            instance = cheapest_obj

        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        cheapest_obj = self.get_cheapest_card(instance)

        if cheapest_obj != instance:
            instance = cheapest_obj

        if instance.seller == request.user:
            return Response(
                data="본인의 상품을 구매할 수 없습니다.", 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(data="구매에 성공했습니다.", status=status.HTTP_204_NO_CONTENT)
