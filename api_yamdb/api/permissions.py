from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminRoleOrStaff(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff) or (request.user.role == 'admin')


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user



class IsAdminUser(BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)