from datetime import datetime, timedelta

from rest_framework import serializers
from django.utils import timezone

from photo_cards.models import RegisteredPhotoCard


class PhotoCardSalesSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(write_only=True)

    class Meta:
        model = RegisteredPhotoCard
        fields = "__all__"
        read_only_fields = ["seller", "fee", "due_date"]

    def validate(self, attrs):
        user = self.context["request"].user
        price = attrs.get("price")
        duration = attrs.pop("duration")

        if not price:
            raise serializers.ValidationError({"price": "가격 입력은 필수입니다."})
        if not duration:
            raise serializers.ValidationError({"duration": "판매기한 입력은 필수입니다."})
        if price % 500 != 0:
            raise serializers.ValidationError({"price": "가격은 500원 단위여야합니다."})

        # seller_id 추가
        attrs["seller_id"] = user.id

        # fee 계산
        attrs["fee"] = price * 0.2

        # due_date 계산
        attrs["due_date"] = datetime.now() + timedelta(days=duration)

        # duration 필드 제거
        attrs.pop("duration", None)

        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class RegisteredPhotoCardListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="photo_card.title")
    release_type = serializers.CharField(source="photo_card.release_type")
    group_name = serializers.CharField(source="photo_card.group_name")
    member_name = serializers.CharField(source="photo_card.member_name")

    class Meta:
        model = RegisteredPhotoCard
        fields = [
            "id",
            "photo_card_id",
            "price",
            "fee",
            "title",
            "release_type",
            "group_name",
            "member_name",
        ]


class RegisteredPhotoCardDetailSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    recent_transactions = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.price + obj.fee
    
    def get_recent_transactions(self, obj):
        # 가장 최근 거래가 5개 구하기
        queryset = RegisteredPhotoCard.objects.filter(
            state=RegisteredPhotoCard.SOLD,
            photo_card_id=obj.photo_card.id,
        ).order_by("sold_date")[:5]

        return queryset.values("sold_date", "price")

    class Meta:
        model = RegisteredPhotoCard
        fields = [
            "id",
            "price",
            "fee",
            "total_price",
            "recent_transactions",
        ]


class RegisteredPhotoCardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredPhotoCard
        fields = ["buyer", "state", "sold_date"]
        read_only_fields = ["buyer", "state", "sold_date"]

    def update(self, instance, validated_data):
        # buyer를 현재 요청 사용자로 설정
        instance.buyer = self.context['request'].user
        # state를 'sold'로 변경
        instance.state = RegisteredPhotoCard.SOLD
        # sold_date를 현재 시간으로 설정
        instance.sold_date = timezone.now()

        instance.save()
        return instance
    
    def validate(self, data):
        if self.instance.state != RegisteredPhotoCard.AVAILABLE:
            raise serializers.ValidationError("구매 가능한 상품이 아닙니다.")
        return data
