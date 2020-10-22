from django.shortcuts import render

from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from titles import Title
from .serializers import ReviewSerializer, CommentSerializer, CategorySerializer, GenreSerializer, TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, pk=title_id).reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        reviews_set = get_object_or_404(Title, pk=title_id).reviews
        review_id = self.kwargs['review_id']
        return get_object_or_404(reviews_set, pk=review_id).comments

    def perform_create(self, serializer):
        post_id = self.kwargs['review_id']
        author = self.request.user
        post = get_object_or_404(Title, pk=post_id)
        serializer.save(author=author, post=post)