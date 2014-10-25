from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_organizer

class IsEventOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user
