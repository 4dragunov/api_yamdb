from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (ReviewViewSet, CommentViewSet, UserViewSet,
                       ConfirmationCodeView, UserLoginView, CategoryViewSet,
                       GenreViewSet, TitleViewSet)

v1_patterns = ([
    path('auth/email', ConfirmationCodeView.as_view()),
    path('auth/token', UserLoginView.as_view()),
])


v1_router = DefaultRouter()
v1_router.register(r'titles', TitleViewSet, basename='TitlesView')
# v1_router.register(r'titles/(P<title_id>\.+)', TitleViewSet, basename='TitleView')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='ReviewsView')
# v1_router.register(r'titles/(P<title_id>\.+)/(P<review_id>\.+)', ReviewViewSet, basename='ReviewView')
v1_router.register(r'titles/(P<titles_id>\.+)/(?P<review_id>.+)/comments', CommentViewSet, basename='CommentsView')
# v1_router.register(
#     r'titles/(P<title_id>\.+)/(?P<review_id>.+)/comments/(?P<comment_id>.+)',
#     CommentViewSet,
#     basename='CommentView'
# )
v1_router.register(r'users', UserViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/', include(v1_router.urls)),
    ]