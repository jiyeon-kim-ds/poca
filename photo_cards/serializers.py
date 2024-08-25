import math
from datetime import datetime, timedelta

from rest_framework import serializers

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
        

    # def create(self, validated_data):
    #     user = self.context["request"].user
    #     duration = validated_data.pop("duration")

    #     validated_data["seller_id"] = user.id
    #     validated_data["fee"] =validated_data["price"] * 0.2
    #     validated_data["due_date"] = datetime.now() + timedelta(days=duration)

    #     return super().create(validated_data)
