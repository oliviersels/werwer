from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.tests.test_serializer import HyperlinkedForeignKeySourceSerializer
from werapp.models import Player, MagicGame, GameRound, GameMatch, GamePlayer


class PlayerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "url", "first_name", "last_name", "username", "email", "dcinumber", "is_judge", "gameplayer_set")

class MagicGameSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = MagicGame
        fields = ("id", "url", "name", "date", "is_paid", "game_type", "pairing_method", "gameround_set", "gameplayer_set")

class GameRoundSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = GameRound
        fields = ("id", "url", "game", "gamematch_set")

class GameMatchSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = GameMatch
        fields = ("id", "url", "round", "gameplayer_set")

class GamePlayerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = GamePlayer
        fields = ("id", "url", "player", "magicgame", "matches")
