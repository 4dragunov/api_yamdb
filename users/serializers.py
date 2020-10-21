from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "role",
            "email",
            "first_name",
            "last_name",
            "bio",
        )



class UserEmailSerializer(serializers.Serializer):
    """Сериализатор email пользователя"""
    email = serializers.EmailField(required=True)


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор email пользователя"""
    email = serializers.EmailField(required=True)
    secret = serializers.CharField(required=True)

