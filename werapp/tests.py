from django.test import TestCase

# Create your tests here.
from django.utils.timezone import now
from werapp.enums import EventType, PairingMethod
from werapp.models import Player, Event, RandomMatchesRequest, Round, Participant
from werapp.tasks import create_random_matches


class CreateRandomMatchesTaskTest(TestCase):

    def setUp(self):
        # Create dummy players and initial event setup
        self.player_dauntless = Player.objects.create_user('dauntless', 'dauntless@lostfleet.com', 'password')
        self.player_fearless = Player.objects.create_user('fearless', 'fearless@lostfleet.com', 'password')
        self.player_courageous = Player.objects.create_user('courageous', 'courageous@lostfleet.com', 'password')
        self.player_valiant = Player.objects.create_user('valiant', 'valiant@lostfleet.com', 'password')
        self.player_relentless = Player.objects.create_user('relentless', 'relentless@lostfleet.com', 'password')
        self.player_victorious = Player.objects.create_user('victorious', 'victorious@lostfleet.com', 'password')
        self.player_dreadnaught = Player.objects.create_user('dreadnaught', 'dreadnaught@lostfleet.com', 'password')
        self.player_invincible = Player.objects.create_user('invincible', 'invincible@lostfleet.com', 'password')

        # Initial event
        self.event = Event.objects.create(name='Test', date=now(), event_type=EventType.CASUAL_LIMITED,
                                             pairing_method=PairingMethod.SWISS, nr_of_rounds=3)

        # Add players as participants
        self.participant_dauntless = Participant.objects.create(player=self.player_dauntless, event=self.event)
        self.participant_fearless = Participant.objects.create(player=self.player_fearless, event=self.event)
        self.participant_courageous = Participant.objects.create(player=self.player_courageous, event=self.event)
        self.participant_valiant = Participant.objects.create(player=self.player_valiant, event=self.event)
        self.participant_relentless = Participant.objects.create(player=self.player_relentless, event=self.event)
        self.participant_victorious = Participant.objects.create(player=self.player_victorious, event=self.event)
        self.participant_dreadnaught = Participant.objects.create(player=self.player_dreadnaught, event=self.event)
        self.participant_invincible = Participant.objects.create(player=self.player_invincible, event=self.event)

    def test_initial_random_matches(self):
        # Create the first round
        round = Round.objects.create(event=self.event)

        # Create the random matches request
        random_matches_request = RandomMatchesRequest.objects.create(round=round)

        # Run the task
        create_random_matches(random_matches_request.id)

        # Check the results
        matches = round.match_set.all()
        players = []
        self.assertEqual(len(matches), 4)  # Expect 4 rounds
        for match in matches:
            for player in match.participant_set.all():
                self.assertNotIn(player, players)  # Every player should be unique
                players.append(player)
        self.assertEqual(len(players), 8)  # Expect 8 players

    def test_initial_random_matches_with_bye(self):
        pass
