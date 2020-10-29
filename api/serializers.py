from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review

from titles.models import Category, Genre, Title

from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    title = serializers.SlugRelatedField(slug_field='pk', read_only=True)

    class Meta:
        fields = ('title', 'id', 'text', 'author', 'score', 'pub_date')
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['author', 'title']
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


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
    email = serializers.EmailField(required=True)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    secret = serializers.CharField(required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        fields = (
            'id', 'name', 'category', 'genre', 'year', 'description', 'rating')
        model = Title
