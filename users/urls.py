from django.urls import path, include

from .views import ConfirmationCodeView, UserLoginView

v1_patterns = ([
    path('auth/email', ConfirmationCodeView.as_view()),
    path('auth/token', UserLoginView.as_view()),
])


urlpatterns = [
    path('v1/', include(v1_patterns))
]