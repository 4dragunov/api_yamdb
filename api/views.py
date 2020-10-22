from django.shortcuts import render
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

   