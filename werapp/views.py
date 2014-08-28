# Create your views here.
from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from werapp.enums import GameType, PairingMethod
from werapp.models import Player, MagicGame, GameRound, GameMatch, GamePlayer, RandomMatchesRequest

from werapp.serializers import PlayerSerializer, MagicGameSerializer, GameRoundSerializer, GameMatchSerializer, \
    GamePlayerSerializer, RandomMatchesRequestSerializer
from werapp.tasks import create_random_matches


class PlayerViewSet(ModelViewSet):
    model = Player
    serializer_class = PlayerSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name', 'dcinumber')

class MagicGameViewSet(ModelViewSet):
    model = MagicGame
    serializer_class = MagicGameSerializer

class GameRoundViewSet(ModelViewSet):
    model = GameRound
    serializer_class = GameRoundSerializer

class GameMatchViewSet(ModelViewSet):
    model = GameMatch
    serializer_class = GameMatchSerializer

class GamePlayerViewSet(ModelViewSet):
    model = GamePlayer
    serializer_class = GamePlayerSerializer

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
        kwargs['enums'] = (GameType, PairingMethod,)
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

class GamesOverviewView(TemplateView):
    template_name = "partials/games-overview.html"

class NewGameView(TemplateView):
    template_name = "partials/new-game.html"

class GameView(TemplateView):
    template_name = "partials/game.html"

class GamePlanningView(TemplateView):
    template_name = "partials/game-planning.html"

class StartEventConfirmView(TemplateView):
    template_name = "partials/start-event-confirm.html"

class GameDraftView(TemplateView):
    template_name = "partials/game-draft.html"

class ConfirmCancelModalView(TemplateView):
    template_name = "partials/confirm-cancel-modal.html"

class GameRoundView(TemplateView):
    template_name = "partials/game-round.html"
