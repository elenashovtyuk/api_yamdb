from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import sign_up, get_jwt_token, UserViewSet, APIUser

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/users/me/', APIUser.as_view(), name='me'),
    path('v1/', include(router.urls)),
]