# from rest_framework import serializers
#
# from .models import User
#
# class UserSerializer(serializers.ModelSerializer):
#     # username = serializers.SlugRelatedField(
#     #     read_only=True,
#     #     slug_field='username'
#     # )
#
#     class Meta:
#         model = User
#         fields = (
#             "id",
#             "username",
#             "role",
#             "email",
#             "first_name",
#             "last_name",
#             "bio",
#         )
#
#
#
# class UserEmailSerializer(serializers.Serializer):
#     """Сериализатор email пользователя для выдачи секретного кода"""
#     email = serializers.EmailField(required=True)
#
#
# class UserLoginSerializer(serializers.Serializer):
#     """Сериализатор email и секретного кода пользователя для JWT"""
#     email = serializers.EmailField(required=True)
#     secret = serializers.CharField(required=True)
#
