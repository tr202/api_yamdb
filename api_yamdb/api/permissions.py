from rest_framework.permissions import BasePermission


class IsAdminModeratorOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            if request.method in {'POST', 'PATCH', 'DELETE'}:
                return True
            return request.user.is_admin or request.user.is_moderator
        return False

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return (
                request.user.is_owner(obj.author)
                or request.user.is_admin
                or request.user.is_moderator
            )
        return False


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        is_user = bool(request.user and request.user.is_authenticated)
        return request.user.is_admin if is_user else False

    def has_object_permission(self, request, view, obj):
        is_user = bool(request.user and request.user.is_authenticated)
        return request.user.is_admin if is_user else False


class IsAdminRoleOrModerator(IsAdminRole):
    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return (
                request.user.is_admin
                or request.user.is_moderator
            )
        return False
