import secrets
import string

import django_filters
from django.core.mail import send_mail
from rest_framework.decorators import action

from .filters import TitleFilter
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from rest_framework.response import Response
from rest_framework import status, filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from .models import Title, Category, Genre
from .permissions import IsAdmin
from .serializers import ReviewSerializer, CommentSerializer,\
    UserEmailSerializer, UserLoginSerializer, UserSerializer,\
    CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    # permission_classes = [IsAdminOrReadOnly]
    queryset = Title.objects.all()
    # lookup_field = "id"
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter


    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist("genre")
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(category=category,
                        genre=genres
                        )

    #     print(request.data)
    #     data = request.data
    #     category_slug = data.get('category')
    #     category = get_object_or_404(Category, name=category_slug)
    #     print(category)
    #     genre_slugs = data.get('genre')
    #     print(genre_slugs)
    #     genres = []
    #     for slug in genre_slugs:
    #         genres += get_object_or_404(Genre, name=slug)
    #     print(genres)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     print(serializer.data)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     serializer.save()


class CategoryViewSet(viewsets.ModelViewSet):
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
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return get_object_or_404(Title, pk=title_id).reviews

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(secrets.choice(chars) for _ in range(size))


class ConfirmationCodeView(APIView):
    '''Обработка POST запроса на получение Confirmation code'''

    def post(self, request):
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
    '''Обработка POST запроса на получение JWT по email и секретному коду'''

    def post(self, request):
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
    '''Модель обработки запросов user'''
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
