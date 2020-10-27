import secrets
import string

import django_filters
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status, filters, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review
from titles.models import Title, Category, Genre
from users.models import User
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, IsAdminOrStaff, IsAdmin
from .serializers import (ReviewSerializer, CommentSerializer,
                          UserEmailSerializer, UserLoginSerializer,
                          UserSerializer,
                          CategorySerializer, GenreSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """"Модель обработки запросов к произведениям"""
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        """"Создание нового произведения, возможно только администротором"""
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist("genre")
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(category=category,
                        genre=genres
                        )

    def perform_update(self, serializer):
        """"Изменение характеристик существующего произведения,
        возможно только администротором"""
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist("genre")
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(category=category,
                        genre=genres
                        )


class CategoryViewSet(viewsets.ModelViewSet):
    """Модель обработки категорий"""
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(viewsets.ModelViewSet):
    """Модель обработки жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    """Модель обработки отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(author=self.request.user,
                                 title=title).exists():
            raise ValidationError("Вы уже оставили отзыв")
        serializer.save(author=self.request.user, title=title)
        title.rating = Review.objects.filter(title=title).aggregate(Avg(
            "score"))["score__avg"]
        title.save(update_fields=["rating"])

    def perform_update(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
        title.rating = Review.objects.filter(title=title).aggregate(Avg(
            "score"))["score__avg"]
        title.save(update_fields=["rating"])


class CommentViewSet(viewsets.ModelViewSet):
    """Модель обработки комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(chars) for _ in range(size))


class ConfirmationCodeView(APIView):

    def post(self, request):
        """Обработка POST запроса на получение Confirmation code"""
        serializer = UserEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            if User.objects.filter(email=email):
                return Response('Пользователь уже зарегестрирован в системе',
                                status=status.HTTP_410_GONE)
            secret = id_generator()
            User.objects.create(email=email, secret=secret)
            send_mail('Ваш секретный код', secret,
                      'admin@yamdb.com', [email],
                      fail_silently=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """ Модель авторизации пользователя """

    def post(self, request):
        """Обработка POST запроса на получение JWT по email и секретному коду"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            secret = serializer.data['secret']

            user = get_object_or_404(User, email=email)
            if user.secret != secret:
                return Response('Вы отправили неверный секретный код',
                                status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)  # получаем токен

            return Response(
                {"access": str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Модель обработки запросов пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin, IsAuthenticated,)
    pagination_class = PageNumberPagination
    lookup_field = "username"

    @action(detail=False, methods=['PATCH', 'GET'],
            permission_classes=(IsAuthenticated,))
    def me(self, request, ):
        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
