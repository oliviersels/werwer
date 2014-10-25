from django.db.models import Q
from rest_framework.filters import BaseFilterBackend
from werapp.models import Event, Participant


class RoundFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        events = [participant.event for participant in Participant.objects.filter(player=request.user)]
        return queryset.filter(Q(event__in=events) | Q(event__organizer=request.user))
