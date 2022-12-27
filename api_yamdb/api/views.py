from django.shortcuts import get_object_or_404
from rest_framework import (
    permissions,
    viewsets
)
from reviews.models import Title, Review, Comment

from .permissions import (
    IsAuthorOrModeratorOrAdminOrReadOnly
)
from .serializers import (
    ReviewSerializer,
    ReviewUpdateSerializer,
    CommentSerializer
)
from django.core.mail import send_mail
from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Avg
import random

from users.models import User
from .serializers import SendCodeSerializer, CheckConfirmationCodeSerializer, UserSerializer
from rest_framework import filters, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from .filters import FilterForTitle
from .mixins import CLDViewSet

from .permissions import (IsAdminOrReadOnly,)
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          ReadOnlyTitleSerializer,
                          TitleSerializer)


class CategoryViewSet(CLDViewSet):
    """Отображение действий с категориями произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class GenreViewSet(CLDViewSet):
    """Отображение действий с жанрами произведений"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Отображение действий с произведениями"""
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterForTitle

    def get_serializer_class(self):
        if self.action in ('list', 'retriev'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ReviewUpdateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy',):
            return (IsAuthorOrModeratorOrAdminOrReadOnly(),)
        if self.action == 'create':
            return (permissions.IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action not in ('list', 'retrieve',):
            return (IsAuthorOrModeratorOrAdminOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
def sign_up(request):
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email')
    username = request.data.get('username')
    if User.objects.filter(username=username, email=email).exists():
        return Response(
            serializer.initial_data, status=status.HTTP_200_OK
        )
    if serializer.is_valid():
        serializer.save()
        confirmation_code = ''.join(
            map(str, random.sample(range(10), 6))
        )
        User.objects.filter(email=email).update(
            confirmation_code=make_password(
                confirmation_code, salt=None, hasher='default'
            )
        )

        mail_subject = 'Код подтверждения на Yamdb.ru'
        message = f'Ваш код подтверждения: {confirmation_code}'
        send_mail(
            mail_subject, message, 'Yamdb.ru <mail@yamdb.ru>', [email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['POST'])
def get_jwt_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    serializer = CheckConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.data)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                serializer.errors, status=status.HTTP_404_NOT_FOUND
            )
        if check_password(confirmation_code, user.confirmation_code):
            print(confirmation_code)
            token = AccessToken.for_user(user)
            return Response(
                {'token': f'{token}'}, status=status.HTTP_200_OK
            )
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'delete', 'patch',)

    @action(
        methods=('get', 'patch',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                user, partial=True, data=request.data
            )
            if serializer.is_valid():
                serializer.save(role=request.user.role)
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
