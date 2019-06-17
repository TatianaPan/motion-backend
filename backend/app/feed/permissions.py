from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous and request.user == obj.user:
            return True
        return False
