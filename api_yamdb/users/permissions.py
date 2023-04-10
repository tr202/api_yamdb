from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        is_user = bool(request.user and request.user.is_authenticated)
        if is_user:
            role = request.user.role
            is_superuser = request.user.is_superuser
            return (role == 'admin' or is_superuser)
        return False
