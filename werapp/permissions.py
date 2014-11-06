from braces.views._access import AccessMixin
from django.contrib.auth.views import redirect_to_login
from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_organizer

class IsEventOrganizer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer == request.user

class OrganizerRequiredMixin(AccessMixin):
    """
    Mixin allows you to require a user with `is_organizer` set to True.
    """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_organizer:  # If the user is not an organizer
            return redirect_to_login(request.get_full_path(),
                                     login_url='wersite-not-an-organizer')  # Special 'login' page

        return super(OrganizerRequiredMixin, self).dispatch(
            request, *args, **kwargs)
