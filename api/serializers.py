from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.validators import UniqueValidator

from reviews.models import Comment, Review

from titles.models import Category, Genre, Title

from users.models import User


class ReviewSerializer(serializers.ModelSerializer):



    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        author = self.context["request"].user
        title_id = self.context.get('request').parser_context['kwargs'][
            'title_id']
        if (Review.objects.filter(author=author, title=title_id).exists() and
                self.context["request"].method != "PATCH"):
            raise serializers.ValidationError("Вы уже оставили отзыв")

        return data


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
