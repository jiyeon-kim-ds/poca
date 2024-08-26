from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    회원가입에 사용하는 serializer
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
