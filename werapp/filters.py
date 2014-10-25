from django.db.models import Q
from rest_framework.filters import BaseFilterBackend
from werapp.models import Event, Participant

class OrganizerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(organizer=request.user)


class EventOrganizerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(event__organizer=request.user)


class RoundEventOrganizerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(round__event__organizer=request.user)
