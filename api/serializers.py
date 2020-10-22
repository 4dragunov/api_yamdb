from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.models import Category, Genre
from reviews.models import Review, Comment
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # TODO AS:
    # title = SlugRelatedField(slug_field='pass', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # TODO AS:
    # title = SlugRelatedField(slug_field='pass', read_only=True)
    # review = SlugRelatedField(slug_field='pass', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username'
    # )

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
    """Сериализатор email пользователя для выдачи секретного кода"""
    email = serializers.EmailField(required=True)


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор email и секретного кода пользователя для JWT"""
    email = serializers.EmailField(required=True)
    secret = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category







class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.Serializer):
    pass

