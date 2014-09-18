from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone
from werapp.enums import EventType, PairingMethod, EventState, RandomMatchesRequestState


class Player(AbstractUser):
    dcinumber = models.CharField(max_length=250, blank=True)
    is_judge = models.BooleanField(default=False)

    objects = UserManager()

class Event(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField(default=timezone.now)
    event_type = models.CharField(max_length=250, choices=EventType.choices)
    pairing_method = models.CharField(max_length=250, choices=PairingMethod.choices)
    is_paid = models.BooleanField(default=True)
    state = models.CharField(max_length=250, choices=EventState.choices, default=EventState.PLANNING)
    nr_of_rounds = models.IntegerField(null=True, blank=True)

class Round(models.Model):
    event = models.ForeignKey(Event)

class Match(models.Model):
    round = models.ForeignKey(Round)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)

    def points_for_participant(self, participant):
        if self.wins == 0 and self.losses == 0 and self.draws == 0:
            # No results entry yet
            return 0
        if participant == self.participant_set.all()[0]:
            player_wins = self.wins
            player_losses = self.losses
        else:
            player_wins = self.losses
            player_losses = self.wins

        if player_wins > player_losses:
            return 3
        elif player_losses > player_wins:
            return 0
        else:
            return 1

class Participant(models.Model):
    player = models.ForeignKey(Player)
    event = models.ForeignKey(Event)
    matches = models.ManyToManyField(to=Match)

    class Meta:
        unique_together = ("player", "event")

    @property
    def points(self):
        # Make a separate function for points as it is often
        # used and the other score statistics take more time to calculate.
        return sum(match.points_for_participant(self) for match in self.matches.all())

    @property
    def score(self):
        return {
            'points': self.points,
            'opponents_match_win_percentage': 50,
        }

class RandomMatchesRequest(models.Model):
    round = models.ForeignKey(Round)
    state = models.CharField(max_length=250, choices=RandomMatchesRequestState.choices, default=RandomMatchesRequestState.NEW)
