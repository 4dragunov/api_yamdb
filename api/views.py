import django_filters
import secrets
import string

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status, filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from titles.models import Title, Category, Genre
from users.models import User
from reviews.models import Review
from .filters import TitleFilter

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsAdmin, \
    ReviewPermissions
from .serializers import ReviewSerializer, CommentSerializer, \
    UserEmailSerializer, UserLoginSerializer, UserSerializer, \
    CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist("genre")
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(category=category,
                        genre=genres
                        )

    def perform_update(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug)
        genre_slug = self.request.POST.getlist("genre")
        genres = Genre.objects.filter(slug__in=genre_slug)
        serializer.save(category=category,
                        genre=genres
                        )


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
    queryset = Review.objects.all()

    # def get_queryset(self):
    #     # title_id = self.kwargs['title_id']
    #     title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
    #     print(title)
    #     print(title.reviews)
    #     return title.reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

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
