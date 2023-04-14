from rest_framework.permissions import BasePermission, SAFE_METHODS

SAFE_METHODS_SET = set(SAFE_METHODS)


def safe_method(request):
    if request.method in SAFE_METHODS_SET:
        return True


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS_SET:
            return True
        if bool(request.user and request.user.is_authenticated):
            if request.method in {'POST', 'PATCH', 'DELETE'}:
                return True
            return request.user.is_admin or request.user.is_moderator
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS_SET:
            return True
        if bool(request.user and request.user.is_authenticated):
            return (
                request.user.is_owner(obj.author)
                or request.user.is_admin
                or request.user.is_moderator
            )
        return False


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS_SET:
            return True
        is_user = bool(request.user and request.user.is_authenticated)
        return request.user.is_admin if is_user else False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS_SET:
            return True
        is_user = bool(request.user and request.user.is_authenticated)
        return request.user.is_admin if is_user else False


class IsAdminRoleOrModerator(IsAdminRole):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS_SET:
            return True
        if bool(request.user and request.user.is_authenticated):
            return (
                request.user.is_admin
                or request.user.is_moderator
            )
        return False
