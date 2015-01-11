# Create your views here.
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.views.generic.base import TemplateView, RedirectView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from wallet.enums import TransactionType

from werapp.enums import EventType, PairingMethod, EventState, RequestState
from werapp.filters import OrganizerFilterBackend, EventOrganizerFilterBackend, RoundEventOrganizerFilterBackend
from werapp.models import Player, Event, Round, Match, Participant, RandomMatchesRequest, EndOfEventMailingRequest, \
    ManualMatchesRequest, Organization, EndEventRequest
from werapp.permissions import IsOrganizer, IsEventOrganizer, OrganizerRequiredMixin
from werapp.serializers import PlayerSerializer, EventSerializer, RoundSerializer, MatchSerializer, \
    ParticipantSerializer, RandomMatchesRequestSerializer, EndOfEventMailingRequestSerializer, PublicEventSerializer, \
    ManualMatchesRequestSerializer, EndEventRequestSerializer
from werapp.tasks import create_random_matches, end_of_event_mailing, create_manual_matches, end_event


class PlayerMeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('player-detail', kwargs={'pk': self.request.user.pk})


class PlayerViewSet(ModelViewSet):
    model = Player
    queryset = Player.objects.all()
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
        obj.organization = Organization.objects.get()


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

    def pre_save(self, obj):
        if obj.pay_with_credits:
            obj.do_pay_with_credits()


class RandomMatchesRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = RandomMatchesRequest
    queryset = RandomMatchesRequest.objects.all()
    serializer_class = RandomMatchesRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (RoundEventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            create_random_matches.delay(obj.id)

class ManualMatchesRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = ManualMatchesRequest
    queryset = ManualMatchesRequest.objects.all()
    serializer_class = ManualMatchesRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (RoundEventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            create_manual_matches.delay(obj.id)

class EndOfEventMailingRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = EndOfEventMailingRequest
    queryset = EndOfEventMailingRequest.objects.all()
    serializer_class = EndOfEventMailingRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (EventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            end_of_event_mailing.delay(obj.id)

class EndEventRequestViewSet(OnlyOrganizerPreSaveMixin, ModelViewSet):
    model = EndEventRequest
    queryset = EndEventRequest.objects.all()
    serializer_class = EndEventRequestSerializer
    permission_classes = (IsAuthenticated, IsOrganizer, IsEventOrganizer)
    filter_backends = (EventOrganizerFilterBackend,)

    def post_save(self, obj, created=False):
        if created:
            # Create the random matches task
            end_event.delay(obj.id)


class WerView(LoginRequiredMixin, OrganizerRequiredMixin, TemplateView):
    template_name = "wer.html"

class DynamicJavascript(TemplateView):
    template_name = "js/dynamic-javascript.js"

    def get_context_data(self, **kwargs):
        kwargs['enums'] = (EventType, PairingMethod, EventState, RequestState)
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

class EventRoundManualMatchesView(TemplateView):
    template_name = "partials/event-round-manual-matches.html"

class EventStandingsView(TemplateView):
    template_name = "partials/event-standings.html"

class EventConclusionView(TemplateView):
    template_name = "partials/event-conclusion.html"

class LoginPartialView(TemplateView):
    template_name = "partials/login.html"
