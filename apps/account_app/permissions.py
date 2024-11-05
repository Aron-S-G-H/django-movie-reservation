from rest_framework import permissions


class UserHasPermissionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_active:
            if view.action in ['list', 'retrieve']:
                return request.user.is_staff
            return request.user.is_staff or request.user.id == int(view.kwargs.get('pk'))
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user.id == obj.id
