from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated and request.user.is_active:
            if view.action == 'create':
                return request.user.is_staff
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class ReservationCustomPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_active:
            if request.method in permissions.SAFE_METHODS:
                return request.user.is_staff
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.id == obj.user.id
