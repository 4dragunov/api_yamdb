from django.urls import path, include

from .views import Confirmation_code

v1_patterns = ([
    path('auth/email', Confirmation_code.as_view()),
])


urlpatterns = [
    path('v1/', include(v1_patterns))
]