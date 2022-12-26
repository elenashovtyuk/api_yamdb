from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    # в методе has_permission проверяем - если метод запроса безопасный
    # или(пользователь аутентифицирован и
    # является администратором или суперюзером),
    # то запрос разрешен
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser))
        )
    # после создания кастомного пермишн,
    # добавляем его в аттрибут permission_classes
    # в соответствующие представления
