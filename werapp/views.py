# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.views.generic.base import TemplateView, RedirectView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from werapp.enums import EventType, PairingMethod, EventState, RandomMatchesRequestState
from werapp.filters import OrganizerFilterBackend, EventOrganizerFilterBackend, RoundEventOrganizerFilterBackend
from werapp.models import Player, Event, Round, Match, Participant, RandomMatchesRequest, EndOfEventMailingRequest
from werapp.permissions import IsOrganizer, IsEventOrganizer
from werapp.serializers import PlayerSerializer, EventSerializer, RoundSerializer, MatchSerializer, \
    ParticipantSerializer, RandomMatchesRequestSerializer, EndOfEventMailingRequestSerializer, PublicEventSerializer
from werapp.tasks import create_random_matches, end_of_event_mailing


class PlayerMeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('player-detail', kwargs={'pk': self.request.user.pk})


class PlayerViewSet(ModelViewSet):
    model = Player
    serializer_class = PlayerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name', 'dcinumber')
    permission_classes = (IsAuthenticated,)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer,)
    filter_backends = (OrganizerFilterBackend,)

    def pre_save(self, obj):
        try:
            if obj.organizer:
                return
        except Player.DoesNotExist:
            pass
        obj.organizer = self.request.user


class PublicEventViewSet(ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = PublicEventSerializer
    permission_classes = (AllowAny,)


class OnlyOrganizerPreSaveMixin(object):
    def pre_save(self, obj):
        if obj.organizer != self.request.user:
            raise PermissionDenied()
        return super(OnlyOrganizerPreSaveMixin, self).pre_save(obj)


class RoundViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (EventOrganizerFilterBackend,)


class MatchViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (RoundEventOrganizerFilterBackend,)


class ParticipantViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (EventOrganizerFilterBackend,)


class RandomMatchesRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = RandomMatchesRequest
    serializer_class = RandomMatchesRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (RoundEventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            create_random_matches.delay(obj.id)


class EndOfEventMailingRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = EndOfEventMailingRequest
    serializer_class = EndOfEventMailingRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (EventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            end_of_event_mailing.delay(obj.id)


class WerView(LoginRequiredMixin, TemplateView):
    template_name = "wer.html"

class DynamicJavascript(TemplateView):
    template_name = "js/dynamic-javascript.js"

    def get_context_data(self, **kwargs):
        kwargs['enums'] = (EventType, PairingMethod, EventState, RandomMatchesRequestState)
        kwargs['client_id'] = settings.OAUTH2_CLIENT_SETTINGS['client_id']
        kwargs['oauth2_endpoint'] = settings.OAUTH2_CLIENT_SETTINGS['oauth2_endpoint']
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

class EventStandingsView(TemplateView):
    template_name = "partials/event-standings.html"

class EventConclusionView(TemplateView):
    template_name = "partials/event-conclusion.html"

class LoginPartialView(TemplateView):
    template_name = "partials/login.html"
