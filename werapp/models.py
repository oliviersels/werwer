from decimal import Decimal
from django.contrib.auth.models import AbstractUser, UserManager, AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from wallet.enums import Currency, TransactionType, TransactionState
from wallet.errors import InsufficientFundsError
from wallet.models import Wallet, Transaction
from werapp.enums import EventType, PairingMethod, EventState, RequestState, ParticipantMatchPlayerNr
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
    is_organizer = models.BooleanField(_('is organizer'), default=False,
       help_text=_('Designates whether this user can create and organize events'))

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

    @property
    def credits_wallet(self):
        credits_wallet = self.wallet_set.filter(currency=Currency.CREDITS).first()
        if credits_wallet is None:
            credits_wallet = Wallet.objects.create(player=self, currency=Currency.CREDITS)
        return credits_wallet

    @property
    def credits(self):
        return self.credits_wallet.amount

    def __unicode__(self):
        if self.pk:
            return "Player [%s] %s" % (self.pk, self.email)
        else:
            return "Player %s" % self.email

class Organization(models.Model):
    name = models.CharField(max_length=250, unique=True)
    organizers = models.ManyToManyField(Player)

    @property
    def credits_wallet(self):
        # Check if the wallet exists
        credits_wallet = self.wallet_set.filter(currency=Currency.CREDITS).first()
        if credits_wallet is None:
            credits_wallet = Wallet.objects.create(organization=self, currency=Currency.CREDITS)
        return credits_wallet

    @property
    def credits(self):
        return self.credits_wallet.amount

    # Normally credits are added by a payment, but for now do it manually
    def add_credits(self, amount):
        # Do the transaction
        return Transaction.objects.do_transaction(wallet_from=None, wallet_to=self.credits_wallet,
                                                  transaction_type=TransactionType.MANUAL, amount=amount)

class Event(models.Model):
    organizer = models.ForeignKey(Player)
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=250)
    date = models.DateField(default=timezone.now)
    event_type = models.CharField(max_length=250, choices=EventType.choices)
    pairing_method = models.CharField(max_length=250, choices=PairingMethod.choices)
    price_support = models.FloatField(default=0)
    price_support_min_points = models.IntegerField(default=0)
    state = models.CharField(max_length=250, choices=EventState.choices, default=EventState.PLANNING)
    nr_of_rounds = models.IntegerField(null=True, blank=True)

    @property
    def current_round(self):
        rounds = self.round_set.all().order_by('-id')
        if len(rounds) > 0:
            return rounds[0]
        return None

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

    def distribute_price_support(self, force=False):
        if not force and self.state == EventState.DONE:
            raise ValueError("You shouldn't distribute price support when the event is done. Override with force=True")

        price_support_distribution = self.get_price_support_distribution()
        total_amount = sum(price_support_distribution.values()) # This should be the same as nr_of_players * price_support

        with atomic():
            organization_wallet = Wallet.objects.select_for_update().filter(organization=self.organization, currency=Currency.CREDITS).first()
            if organization_wallet is None:
                organization_wallet = Wallet.objects.create(organization=self, currency=Currency.CREDITS)
            if organization_wallet.amount < total_amount:
                raise InsufficientFundsError()

            # Do stuff
            for participant_id, amount in price_support_distribution.items():
                if amount > 0:
                    participant = Participant.objects.get(id=participant_id)
                    player = participant.player
                    player_wallet = player.wallet_set.select_for_update().filter(currency=Currency.CREDITS).first()
                    if player_wallet is None:
                        player = Player.objects.select_for_update().get(pk=player.pk)
                        player_wallet = Wallet.objects.create(player=player, currency=Currency.CREDITS)

                    t = Transaction.objects.do_transaction(wallet_from=organization_wallet, wallet_to=player_wallet,
                                                           transaction_type=TransactionType.EVENT_CREDITS, amount=amount)
                    t.participant = participant
                    t.save()


    def __unicode__(self):
        description = "%s (%s)" % (self.name, self.date)
        if self.pk:
            description = ("Event [%s] " % self.pk) + description
        else:
            description = "Event " + description
        return description

class Round(models.Model):
    event = models.ForeignKey(Event)

    @property
    def organizer(self):
        return self.event.organizer

    @property
    def round_nr(self):
        return list(self.event.round_set.all().order_by('id').values_list('id', flat=True)).index(self.id) + 1

    def is_participant(self, player):
        return self.event.participant_set.filter(player=player).exists()

    def __unicode__(self):
        if self.pk:
            return "Round [%s] -%s-" % (self.pk, self.event.name)
        else:
            return "Round -%s-" % self.event.name

class Match(models.Model):
    round = models.ForeignKey(Round)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)

    @property
    def organizer(self):
        return self.round.event.organizer

    @property
    def participant1(self):
        if not hasattr(self, '_participant1'):
            self._participant1 = self.participantmatch_set.select_related('participant')\
                .get(player_nr=ParticipantMatchPlayerNr.PLAYER_1).participant
        return self._participant1

    @property
    def participant2(self):
        if not hasattr(self, '_participant2'):
            self._participant2 = self.participantmatch_set.select_related('participant')\
                .get(player_nr=ParticipantMatchPlayerNr.PLAYER_2).participant
        return self._participant2

    def get_opponent(self, participant):
        if participant == self.participant1:
            return self.participant2
        elif participant == self.participant2:
            return self.participant1
        else:
            return None

    @property
    def bye(self):
        return self.participant_set.count() == 1

    def points_for_participant(self, participant, include_game_points=False):
        if self.bye:
            # Bye counts as 2-0 win
            player_wins = 2
            player_losses = 0
            player_draws = 0
        elif self.wins == 0 and self.losses == 0 and self.draws == 0:
            # No results entry yet
            if not include_game_points:
                return 0
            else:
                return None
        else:
            if participant == self.participant1:
                player_wins = self.wins
                player_losses = self.losses
                player_draws = self.draws
            else:
                player_wins = self.losses
                player_losses = self.wins
                player_draws = self.draws

        if player_wins > player_losses:
            points = 3
        elif player_losses > player_wins:
            points = 0
        else:
            points = 1

        if not include_game_points:
            return points
        else:
            return {
                'match_points': points,
                'game_points': 3 * player_wins + player_draws,
                'games': player_wins + player_draws + player_losses,
            }

    def __unicode__(self):
        description = "Match -%s- " % self.round.event.name
        if self.pk:
            description += "[%s] " % self.pk
        if self.bye:
            description += "%s (Bye)" % self.participant1.player.email
        elif self.participant_set.count() == 2:
            description += "%s vs %s" % (self.participant1.player.email, self.participant2.player.email)
        else:
            description += "(no players)"
        return description


class Participant(models.Model):
    player = models.ForeignKey(Player)
    event = models.ForeignKey(Event)
    matches = models.ManyToManyField(to=Match, through="ParticipantMatch")
    pay_with_credits = models.BooleanField(default=False)
    # The following fields are filled in when the event is done. The on-the-fly calculations can be quite expensive.
    done_price_support = models.FloatField(blank=True, null=True)
    done_points = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("player", "event")

    @property
    def organizer(self):
        return self.event.organizer

    @property
    def price_support(self):
        # How much this player has earned in price support
        if self.done_price_support is not None:
            return self.done_price_support
        return self.event.get_price_support_distribution()[self.id]

    @property
    def points(self):
        # Make a separate function for points as it is often
        # used and the other score statistics take more time to calculate.
        if self.done_points is not None:
            return self.done_points
        return sum(match.points_for_participant(self) for match in self.matches.all())

    @property
    def tie_breakers(self):
        tie_breakers_info = self._get_tie_breakers_info()
        tie_breakers = {
            'match_points': tie_breakers_info['match_points_total'],
            'game_win_percentage': float(tie_breakers_info['game_points_total']) / (3 * tie_breakers_info['games']),
        }
        opponents_match_win_percentages = []
        opponents_game_win_percentages = []
        for opponent in tie_breakers_info['opponents']:
            opponent_tie_breakers_info = opponent._get_tie_breakers_info()
            opponents_match_win_percentages.append(max(0.33, float(opponent_tie_breakers_info['match_points_total']) / (3 * opponent_tie_breakers_info['rounds'])))
            opponents_game_win_percentages.append(float(opponent_tie_breakers_info['game_points_total']) / (3 * opponent_tie_breakers_info['games']))

        tie_breakers['opponents_match_win_percentage'] = float(sum(opponents_match_win_percentages)) / len(opponents_match_win_percentages)
        tie_breakers['opponents_game_win_percentage'] = float(sum(opponents_game_win_percentages)) / len(opponents_game_win_percentages)
        return tie_breakers

    def _get_tie_breakers_info(self):
        tie_breakers_info = {
            'match_points_total': 0,
            'game_points_total': 0,
            'games': 0,
            'rounds': 0,
            'opponents': [],
        }
        for match in self.matches.all().order_by('round__id'):
            points = match.points_for_participant(self, True)
            if points is not None:
                tie_breakers_info['match_points_total'] += points['match_points']
                tie_breakers_info['game_points_total'] += points['game_points']
                tie_breakers_info['games'] += points['games']
                tie_breakers_info['rounds'] += 1
                if not match.bye:
                    tie_breakers_info['opponents'].append(match.get_opponent(self))
        return tie_breakers_info

    @property
    def score(self):
        tie_breakers = self.tie_breakers

        return {
            'points': tie_breakers['match_points'],
            'match_points': tie_breakers['match_points'],
            'opponents_match_win_percentage': tie_breakers['opponents_match_win_percentage'],
            'game_win_percentage': tie_breakers['game_win_percentage'],
            'opponents_game_win_percentage': tie_breakers['opponents_game_win_percentage'],
        }

    @property
    def _has_payed_with_credits(self):
        return self.transaction_set.filter(transaction_type=TransactionType.EVENT_FEE, state=TransactionState.COMPLETED).count() != 0

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

    def do_pay_with_credits(self):
        if not self._has_payed_with_credits:
            transaction = Transaction.objects.do_transaction(
                wallet_from=self.player.credits_wallet, wallet_to=self.event.organization.credits_wallet,
                amount=Decimal("8"), transaction_type=TransactionType.EVENT_FEE
            )
            transaction.participant = self
            transaction.save()
            self.pay_with_credits = True
            self.save()

    def save(self, *args, **kwargs):
        if self._has_payed_with_credits and not self.pay_with_credits:
            raise ValueError('You cannot disable pay_with_credits when the transaction was completed')
        super(Participant, self).save(*args, **kwargs)

    def __unicode__(self):
        description = "Participant "
        if self.pk:
            description += "[%s] " % self.pk
        return description + "%s - %s" % (self.player.email, self.event.name)

class ParticipantMatch(models.Model):
    participant = models.ForeignKey(Participant)
    match = models.ForeignKey(Match)
    player_nr = models.IntegerField()

    def __unicode__(self):
        description = "ParticipantMatch "
        if self.pk:
            description += "[%s] " % self.pk
        return description + "%s - %s - Match [%s]" % (self.player_nr, self.participant.player.email, self.match.pk)

class RandomMatchesRequest(models.Model):
    round = models.ForeignKey(Round)
    state = models.CharField(max_length=250, choices=RequestState.choices, default=RequestState.NEW)

    @property
    def organizer(self):
        return self.round.event.organizer

class ManualMatchesRequest(models.Model):
    round = models.ForeignKey(Round)
    state = models.CharField(max_length=250, choices=RequestState.choices, default=RequestState.NEW)
    participants = models.CommaSeparatedIntegerField(max_length=250,help_text='The ids of ordered participants separated by , ex: "1,4,2,3" means 1 vs 4 and 2 vs 3')

    @property
    def organizer(self):
        return self.round.event.organizer

class EndOfEventMailingRequest(models.Model):
    event = models.ForeignKey(Event)

    @property
    def organizer(self):
        return self.event.organizer

class EndEventRequest(models.Model):
    event = models.ForeignKey(Event)

    @property
    def organizer(self):
        return self.event.organizer
