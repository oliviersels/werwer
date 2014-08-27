from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone
from werapp.enums import GameType, PairingMethod, MagicGameState


class Player(AbstractUser):
    dcinumber = models.CharField(max_length=250, blank=True)
    is_judge = models.BooleanField(default=False)

    objects = UserManager()

class MagicGame(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField(default=timezone.now)
    game_type = models.CharField(max_length=250, choices=GameType.choices)
    pairing_method = models.CharField(max_length=250, choices=PairingMethod.choices)
    is_paid = models.BooleanField(default=True)
    state = models.CharField(max_length=250, choices=MagicGameState.choices, default=MagicGameState.PLANNING)
    nr_of_rounds = models.IntegerField(null=True, blank=True)

class GameRound(models.Model):
    game = models.ForeignKey(MagicGame)

class GameMatch(models.Model):
    round = models.ForeignKey(GameRound)

class GamePlayer(models.Model):
    player = models.ForeignKey(Player)
    magicgame = models.ForeignKey(MagicGame)
    matches = models.ManyToManyField(to=GameMatch)

    class Meta:
        unique_together = ("player", "magicgame")

    def score(self):
        return {
            'points': 0,
            'opponents_match_win_percentage': 50,
        }

