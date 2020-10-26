from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.models import Category, Genre, Title
from reviews.models import Review, Comment
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # TODO AS:
    # title = SlugRelatedField(slug_field='pass', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    # TODO AS:
    # title = SlugRelatedField(slug_field='pass', read_only=True)
    # review = SlugRelatedField(slug_field='pass', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
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

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    # slug = SlugRelatedField(slug_field='slug', read_only=True)
    class Meta:
        fields = ('name', 'slug')
        model = Category





class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = ('id', 'name', 'category', 'genre', 'year', 'description', 'rating')
        model = Title





