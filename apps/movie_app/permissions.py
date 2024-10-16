from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to create objects.
    """
    def has_permission(self, request, view):
        # Check if the request method is 'POST' (create) and the user is admin
        if request.method == 'POST':
            return request.user and request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
