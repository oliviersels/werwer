from rest_framework.fields import IntegerField, FloatField, BooleanField, CharField
from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer, Serializer
from werapp.models import Player, Event, Round, Match, Participant, RandomMatchesRequest, EndOfEventMailingRequest, \
    ManualMatchesRequest, EndEventRequest


class PlayerSerializer(HyperlinkedModelSerializer):
    credits = FloatField(read_only=True)

    class Meta:
        model = Player
        fields = ("id", "url", "first_name", "last_name", "email", "dcinumber", "is_judge", "credits",
                  "participant_set", "event_set")
        read_only_fields = ("event_set", "participant_set")
        write_only_fields = ("email",)

class EventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "url", "organizer", "name", "date", "price_support", "price_support_min_points", "event_type",
                  "pairing_method", "state", "nr_of_rounds", "round_set", "participant_set")
        read_only_fields = ("organizer",)

class PublicEventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ("url", "organizer", "name", "date", "price_support", "price_support_min_points", "event_type",
                  "pairing_method", "state", "nr_of_rounds")
        view_name = 'public-event-detail'

class RoundSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Round
        fields = ("id", "url", "event", "match_set")
        read_only_fields = ("match_set",)

class MatchSerializer(HyperlinkedModelSerializer):
    bye = BooleanField(read_only=True)
    participant1 = HyperlinkedRelatedField(read_only=True, view_name="participant-detail")
    participant2 = HyperlinkedRelatedField(read_only=True, view_name="participant-detail")

    class Meta:
        model = Match
        fields = ("id", "url", "round", "participant_set", "wins", "losses", "draws", "bye", "participant1", "participant2")
        read_only_fields = ("participant_set", "round")

class ParticipantScoreSerializer(Serializer):
    points = IntegerField()
    opponents_match_win_percentage = FloatField()
    game_win_percentage = FloatField()
    opponents_game_win_percentage = FloatField()

class ParticipantSerializer(HyperlinkedModelSerializer):
    score = ParticipantScoreSerializer(read_only=True)
    price_support = FloatField(read_only=True)

    class Meta:
        model = Participant
        fields = ("id", "url", "player", "event", "matches", "score", "price_support", "pay_with_credits")

class RandomMatchesRequestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = RandomMatchesRequest
        fields = ("id", "url", "round", "state")
        read_only_fields = ("state",)

class ManualMatchesRequestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = ManualMatchesRequest
        fields = ("id", "url", "round", "state", "participants")
        read_only_fields = ("state",)

class EndOfEventMailingRequestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = EndOfEventMailingRequest
        fields = ("id", "url", "event",)
        read_only_fields = ("id",)

class EndEventRequestSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = EndEventRequest
        fields = ("id", "url", "event",)
        read_only_fields = ("id",)
