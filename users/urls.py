from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ConfirmationCodeView, UserLoginView, UserViewSet

app_name = 'users'

v1_patterns = ([
    path('auth/email', ConfirmationCodeView.as_view()),
    path('auth/token', UserLoginView.as_view()),
])

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)



urlpatterns = [
    path('v1/', include(v1_patterns)),
    path('v1/', include(router_v1.urls)),
]