from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Review, Comment


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
