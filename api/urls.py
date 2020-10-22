from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import ReviewViewSet, CommentViewSet
from rest_framework.authtoken import views


v1_router = DefaultRouter()
# здесь роут на titles
v1_router.register(r'titles/(P<title_id>\.+)/reviews', ReviewViewSet, basename='ReviewsView')
v1_router.register(r'titles/(P<title_id>\.+)/(P<review_id>\.+)', ReviewViewSet, basename='ReviewView')
v1_router.register(r'titles/(P<title_id>\.+)/(?P<review_id>.+)/comments', CommentViewSet, basename='CommentsView')
v1_router.register(
    r'titles/(P<title_id>\.+)/(?P<review_id>.+)/comments/(?P<comment_id>.+)',
    CommentViewSet,
    basename='CommentView'
)


urlpatterns = [
    path(include(v1_router.urls)),
    # здесь роут авторизации
    ]