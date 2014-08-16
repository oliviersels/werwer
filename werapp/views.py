# Create your views here.
from django.views.generic.base import TemplateView
from rest_framework.viewsets import ModelViewSet
from werapp.models import Player, MagicGame, GameRound, GameMatch, GamePlayer

from werapp.serializers import PlayerSerializer, MagicGameSerializer, GameRoundSerializer, GameMatchSerializer, \
    GamePlayerSerializer


class PlayerViewSet(ModelViewSet):
    model = Player
    serializer_class = PlayerSerializer

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



class WerView(TemplateView):
    template_name = "wer.html"

class HomeView(TemplateView):
    template_name = "partials/home.html"

class PlayerView(TemplateView):
    template_name = "partials/players.html"

class EditPlayerView(TemplateView):
    template_name = "partials/edit-player.html"
