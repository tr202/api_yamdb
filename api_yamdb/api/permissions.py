from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_authenticated):
            if request.method in ['POST', 'PATCH', 'DELETE']:
                return True
            return bool(request.user.role == 'admin'
                        or request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_authenticated):
            return bool(obj.author == request.user or request.user.role == 'admin'
                        or request.user.role == 'moderator')


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        is_user = bool(request.user and request.user.is_authenticated)
        if is_user:
            role = request.user.role
            is_superuser = request.user.is_superuser
            return (role == 'admin' or is_superuser)
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if bool(request.user and request.user.is_authenticated):
            return bool(request.user.role == 'admin'
                        or request.user.role == 'moderator')


class IsAdminRoleOrStaff(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        is_user = bool(request.user and request.user.is_authenticated)
        if is_user:
            role = request.user.role
            is_superuser = request.user.is_superuser
            return (role == 'admin' or is_superuser)
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        is_user = bool(request.user and request.user.is_authenticated)
        if is_user:
            role = request.user.role
            is_superuser = request.user.is_superuser
            return (role == 'admin' or is_superuser)
        return False


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
