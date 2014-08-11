from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.
from django.utils import timezone


class Player(AbstractUser):
    dcinumber = models.CharField(max_length=255, blank=True)
    is_judge = models.BooleanField(default=False)

    objects = UserManager()

class MagicGame(models.Model):
    date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=True)

class GameRound(models.Model):
    game = models.ForeignKey(MagicGame)

class GameMatch(models.Model):
    round = models.ForeignKey(GameRound)

class GamePlayer(models.Model):
    player = models.ForeignKey(Player)
    magicgame = models.ForeignKey(MagicGame)
    matches = models.ManyToManyField(to=GameMatch)
