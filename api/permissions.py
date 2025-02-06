from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsAdminUserOrIsOwnerReadDestroyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return obj.customer == request.user

        if request.method == 'DELETE' and obj.status is False:
            return obj.customer == request.user

        return False


class IsAdminUserOrIsOwnerReadUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return obj.customer == request.user

        if request.method == 'PUT' and obj.order.status is False:
            return obj.customer == request.user

        return False


class IsAdminUserOrIsAuthenticatedCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)

        return False


class IsAdminUserOrIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True

        return obj.id == request.user.id
