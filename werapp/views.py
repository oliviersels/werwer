# Create your views here.
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from werapp.enums import EventType, PairingMethod, EventState, RandomMatchesRequestState
from werapp.models import Player, Event, Round, Match, Participant, RandomMatchesRequest

from werapp.serializers import PlayerSerializer, EventSerializer, RoundSerializer, MatchSerializer, \
    ParticipantSerializer, RandomMatchesRequestSerializer
from werapp.tasks import create_random_matches


class PlayerViewSet(ModelViewSet):
    model = Player
    serializer_class = PlayerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name', 'dcinumber')

class EventViewSet(ModelViewSet):
    model = Event
    serializer_class = EventSerializer

class RoundViewSet(ModelViewSet):
    model = Round
    serializer_class = RoundSerializer

class MatchViewSet(ModelViewSet):
    model = Match
    serializer_class = MatchSerializer

class ParticipantViewSet(ModelViewSet):
    model = Participant
    serializer_class = ParticipantSerializer

class RandomMatchesRequestViewSet(ModelViewSet):
    model = RandomMatchesRequest
    serializer_class = RandomMatchesRequestSerializer

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            create_random_matches.delay(obj.id)

class WerView(TemplateView):
    template_name = "wer.html"

class DynamicJavascript(TemplateView):
    template_name = "js/dynamic-javascript.js"

    def get_context_data(self, **kwargs):
        kwargs['enums'] = (EventType, PairingMethod, EventState, RandomMatchesRequestState)
        return kwargs

class HomeView(TemplateView):
    template_name = "partials/home.html"

class PlayerView(TemplateView):
    template_name = "partials/players.html"

class EditPlayerView(TemplateView):
    template_name = "partials/edit-player.html"

class EditPlayerConfirmView(TemplateView):
    template_name = "partials/edit-player-confirm.html"

class AddPlayerView(TemplateView):
    template_name = "partials/add-player.html"

class EventsOverviewView(TemplateView):
    template_name = "partials/events-overview.html"

class NewEventView(TemplateView):
    template_name = "partials/new-event.html"

class EventView(TemplateView):
    template_name = "partials/event.html"

class EventPlanningView(TemplateView):
    template_name = "partials/event-planning.html"

class StartEventConfirmView(TemplateView):
    template_name = "partials/start-event-confirm.html"

class EventDraftView(TemplateView):
    template_name = "partials/event-draft.html"

class ConfirmCancelModalView(TemplateView):
    template_name = "partials/confirm-cancel-modal.html"

class EventRoundView(TemplateView):
    template_name = "partials/event-round.html"
