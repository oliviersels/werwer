from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from werapp.enums import EventType, PairingMethod, EventState, RandomMatchesRequestState, ParticipantMatchPlayerNr
from werapp.managers import PlayerManager


class Player(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    dcinumber = models.CharField(max_length=250, blank=True)
    is_judge = models.BooleanField(default=False)

    objects = PlayerManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField(default=timezone.now)
    event_type = models.CharField(max_length=250, choices=EventType.choices)
    pairing_method = models.CharField(max_length=250, choices=PairingMethod.choices)
    price_support = models.FloatField(default=0)
    price_support_min_points = models.IntegerField(default=0)
    state = models.CharField(max_length=250, choices=EventState.choices, default=EventState.PLANNING)
    nr_of_rounds = models.IntegerField(null=True, blank=True)

    def get_price_support_distribution(self):
        # Returns a map of price support for each player
        nr_of_players = self.participant_set.count()
        price_support_amount = nr_of_players * self.price_support

        participant_price_support_points = dict()
        for participant in self.participant_set.all():
            price_support_multiplier = 0.0
            for match in participant.matches.all():
                if match.points_for_participant(participant) == 3:
                    price_support_multiplier += 1
                elif match.points_for_participant(participant) == 3:
                    price_support_multiplier += 0.5

            participant_price_support_points[participant.id] = max(0, participant.points - self.price_support_min_points) * price_support_multiplier
        total_participant_price_support_points = sum(participant_price_support_points.values())

        result_distribution = dict()
        for participant in self.participant_set.all():
            if total_participant_price_support_points == 0:
                result_distribution[participant.id] = 0
            else:
                result_distribution[participant.id] = participant_price_support_points[participant.id] / total_participant_price_support_points * price_support_amount
        return result_distribution

class Round(models.Model):
    event = models.ForeignKey(Event)

class Match(models.Model):
    round = models.ForeignKey(Round)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)

    @property
    def participant1(self):
        for participant_match in self.participantmatch_set.all():
            if participant_match.player_nr == ParticipantMatchPlayerNr.PLAYER_1:
                return participant_match.participant

    @property
    def participant2(self):
        for participant_match in self.participantmatch_set.all():
            if participant_match.player_nr == ParticipantMatchPlayerNr.PLAYER_2:
                return participant_match.participant

    @property
    def bye(self):
        return self.participant_set.count() == 1

    def points_for_participant(self, participant):
        if self.bye:
            return 3 # Player has a bye
        if self.wins == 0 and self.losses == 0 and self.draws == 0:
            # No results entry yet
            return 0
        if participant == self.participant1:
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
    matches = models.ManyToManyField(to=Match, through="ParticipantMatch")

    class Meta:
        unique_together = ("player", "event")

    @property
    def price_support(self):
        # How much this player has earned in price support
        return self.event.get_price_support_distribution()[self.id]

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

    def has_received_bye(self):
        for match in self.matches.all():
            if match.participant_set.count() == 1:
                return True
        return False

    def has_played_against(self, otherParticipant):
        for match in self.matches.all():
            for participant in match.participant_set.all():
                if participant.id == otherParticipant.id:
                    return True
        return False

class ParticipantMatch(models.Model):
    participant = models.ForeignKey(Participant)
    match = models.ForeignKey(Match)
    player_nr = models.IntegerField()

class RandomMatchesRequest(models.Model):
    round = models.ForeignKey(Round)
    state = models.CharField(max_length=250, choices=RandomMatchesRequestState.choices, default=RandomMatchesRequestState.NEW)

class EndOfEventMailingRequest(models.Model):
    event = models.ForeignKey(Event)
