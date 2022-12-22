from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        pass

    def has_object_permission(self, request, view, obj):
        pass
    # после создания кастомного пермишн,
    # добавляем его в аттрибут permission_classes
    # в соответствующие представления
