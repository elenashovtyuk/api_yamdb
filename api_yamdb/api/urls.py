from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import send_confirmation_code, get_jwt_token, UserViewSet, APIUser

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/email/', send_confirmation_code, name='get_token'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/users/me/', APIUser.as_view()),
    path('v1/', include(router.urls)),
]