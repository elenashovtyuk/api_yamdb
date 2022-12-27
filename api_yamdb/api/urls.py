from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import sign_up, get_jwt_token, UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet, CommentViewSet


router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet,)
router_v1.register(r'titles',
                TitleViewSet,
                basename='titles')

router_v1.register(r'categories',
                CategoryViewSet,
                basename='categories')

router_v1.register(r'genres',
                GenreViewSet,
                basename='genres')

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_jwt_token, name='send_confirmation_code'),
    path('v1/', include(router.urls)),
]
