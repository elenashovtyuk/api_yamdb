from rest_framework import permissions
from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.objects.filter(id=request.user.id).exists():
            return request.user.is_admin


class IsSuperUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if User.objects.filter(id=request.user.id).exists():
            return request.user.is_superuser or request.user.is_admin


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if (
                request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
        ):
            return True
