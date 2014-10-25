from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return view.action != 'create' or request.user.is_organizer

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.organizer == request.user

class IsAdminOrOrganizer(BasePermission):
    def has_permission(self, request, view):
        return view.action != 'create' or request.user.is_organizer or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        #TODO
        pass

class IsEventOrganizerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user or (request.method in SAFE_METHODS and obj.is_participant(request.user))
