from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (ReviewViewSet, CommentViewSet, UserViewSet,
                       ConfirmationCodeView, UserLoginView, CategoryViewSet,
                       GenreViewSet)

v1_patterns = ([
    path('auth/email', ConfirmationCodeView.as_view()),
    path('auth/token', UserLoginView.as_view()),
])


v1_router = DefaultRouter()
# здесь роут на titles
v1_router.register(r'titles/(P<title_id>\.+)/reviews', ReviewViewSet, basename='ReviewsView')
v1_router.register(r'titles/(P<title_id>\.+)/(P<review_id>\.+)', ReviewViewSet, basename='ReviewView')
v1_router.register(r'titles/(P<title_id>\.+)/(?P<review_id>.+)/comments',
                   CommentViewSet, basename='CommentsView')
v1_router.register(
    r'titles/(P<title_id>\.+)/(?P<review_id>.+)/comments/(?P<comment_id>.+)',
    CommentViewSet,
    basename='CommentView'
)
v1_router.register(r'users', UserViewSet)
v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)



urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/', include(v1_router.urls)),

    ]