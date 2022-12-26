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
