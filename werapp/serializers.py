from rest_framework.fields import IntegerField, FloatField
from rest_framework.serializers import HyperlinkedModelSerializer, Serializer
from rest_framework.tests.test_serializer import HyperlinkedForeignKeySourceSerializer
from werapp.models import Player, Event, Round, Match, Participant, RandomMatchesRequest


class PlayerSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ("id", "url", "first_name", "last_name", "username", "email", "dcinumber", "is_judge", "participant_set")

class EventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "url", "name", "date", "is_paid", "event_type", "pairing_method", "state", "nr_of_rounds",
                  "round_set", "participant_set")

class RoundSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Round
        fields = ("id", "url", "event", "match_set")

class MatchSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ("id", "url", "round", "participant_set", "wins", "losses", "draws")

class ParticipantScoreSerializer(Serializer):
    points = IntegerField()
    opponents_match_win_percentage = FloatField()

class ParticipantSerializer(HyperlinkedModelSerializer):
    score = ParticipantScoreSerializer(read_only = True)

    class Meta:
        model = Participant
        fields = ("id", "url", "player", "event", "matches", "score")

class RandomMatchesRequestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = RandomMatchesRequest
        fields = ("id", "url", "round", "state")
        read_only_fields = ("state",)
