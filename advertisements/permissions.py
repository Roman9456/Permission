from rest_framework.permissions import BasePermission

class CanDeleteAdvertisement(BasePermission):
    """Право доступа для удаления объявления."""

    def has_object_permission(self, request, view, obj):
        """Проверка разрешения для удаления объявления."""

        # Проверяем, является ли пользователь автором объявления
        return obj.creator == request.user