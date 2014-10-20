from django.test import TestCase

# Create your tests here.
from django.utils.timezone import now
from werapp.enums import EventType, PairingMethod, ParticipantMatchPlayerNr
from werapp.models import Player, Event, RandomMatchesRequest, Round, Participant, Match, ParticipantMatch
from werapp.tasks import create_random_matches


class CreateRandomMatchesTaskTest(TestCase):

    def setUp(self):
        # Create dummy players and initial event setup
        self.player_dauntless = Player.objects.create_user('dauntless@lostfleet.com', 'password')
        self.player_fearless = Player.objects.create_user('fearless@lostfleet.com', 'password')
        self.player_courageous = Player.objects.create_user('courageous@lostfleet.com', 'password')
        self.player_valiant = Player.objects.create_user('valiant@lostfleet.com', 'password')
        self.player_relentless = Player.objects.create_user('relentless@lostfleet.com', 'password')
        self.player_victorious = Player.objects.create_user('victorious@lostfleet.com', 'password')
        self.player_dreadnaught = Player.objects.create_user('dreadnaught@lostfleet.com', 'password')
        self.player_invincible = Player.objects.create_user('invincible@lostfleet.com', 'password')

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
        self.assertEqual(len(matches), 4)  # Expect 4 matches
        for match in matches:
            for player in match.participant_set.all():
                self.assertNotIn(player, players)  # Every player should be unique
                players.append(player)
        self.assertEqual(len(players), 8)  # Expect 8 players

    def test_initial_random_matches_with_bye(self):
        # Add another player so we have 9
        player_guardian = Player.objects.create_user('guardian@lostfleet.com', 'password')
        participant_guardian = Participant.objects.create(player=player_guardian, event=self.event)

        # Create the first round
        round = Round.objects.create(event=self.event)

        # Create the random matches request
        random_matches_request = RandomMatchesRequest.objects.create(round=round)

        # Run the task
        create_random_matches(random_matches_request.id)

        # Check the results
        matches = round.match_set.all()
        players = []
        self.assertEqual(len(matches), 5)  # Expect 5 matches
        for match in matches:
            for player in match.participant_set.all():
                self.assertNotIn(player, players)  # Every player should be unique
                players.append(player)
        self.assertEqual(len(players), 9)  # Expect 9 players

    def test_random_matches_with_simple_results(self):
        # Test random matches with some simple results (all wins or losses)
        # Create the first round
        round1 = Round.objects.create(event=self.event)

        # Create the matches manually
        match1 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match2 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match3 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match4 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_2)

        # Create the second round
        round2 = Round.objects.create(event=self.event)

        # Create the random matches request
        random_matches_request = RandomMatchesRequest.objects.create(round=round2)

        # Run the task
        create_random_matches(random_matches_request.id)

        # Check the results
        matches = round2.match_set.all()
        players = []
        self.assertEqual(len(matches), 4)  # Expect 4 matches
        winners = set(list(matches[0].participant_set.all()) + list(matches[1].participant_set.all()))
        losers = set(list(matches[2].participant_set.all()) + list(matches[3].participant_set.all()))

        self.assertSetEqual(winners, {self.participant_dauntless, self.participant_courageous,
                                      self.participant_relentless, self.participant_dreadnaught})
        self.assertSetEqual(losers, {self.participant_fearless, self.participant_valiant,
                                     self.participant_victorious, self.participant_invincible})

    def test_random_matches_with_simple_results_bye(self):
        # Test random matches with some simple results (all wins or losses)
        # Add another player so we have 9
        player_guardian = Player.objects.create_user('guardian@lostfleet.com', 'password')
        participant_guardian = Participant.objects.create(player=player_guardian, event=self.event)

        # Create the first round
        round1 = Round.objects.create(event=self.event)

        # Create the matches manually
        match1 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match2 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match3 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match4 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match5 = Match.objects.create(round=round1)
        ParticipantMatch.objects.create(participant=participant_guardian, match=match5, player_nr=ParticipantMatchPlayerNr.PLAYER_1)

        # Create the second round
        round2 = Round.objects.create(event=self.event)

        # Create the random matches request
        random_matches_request = RandomMatchesRequest.objects.create(round=round2)

        # Run the task
        create_random_matches(random_matches_request.id)

        # Check the results
        matches = round2.match_set.all()
        players = []
        self.assertEqual(len(matches), 5)  # Expect 5 matches
        winners = set(list(matches[0].participant_set.all()) + list(matches[1].participant_set.all()))
        ambiguous1 = matches[2].participant1
        ambiguous2 = matches[2].participant2
        losers = set(list(matches[3].participant_set.all()))
        byes = set(list(matches[4].participant_set.all()))

        # Assert losers not in winners
        self.assertNotIn(self.participant_fearless, winners)
        self.assertNotIn(self.participant_valiant, winners)
        self.assertNotIn(self.participant_victorious, winners)
        self.assertNotIn(self.participant_invincible, winners)
        # Assert winners not in losers
        self.assertNotIn(self.participant_dauntless, losers)
        self.assertNotIn(self.participant_courageous, losers)
        self.assertNotIn(self.participant_relentless, losers)
        self.assertNotIn(self.participant_dreadnaught, losers)
        self.assertNotIn(participant_guardian, losers)
        # Assert winners not in byes
        self.assertNotIn(self.participant_dauntless, byes)
        self.assertNotIn(self.participant_courageous, byes)
        self.assertNotIn(self.participant_relentless, byes)
        self.assertNotIn(self.participant_dreadnaught, byes)
        self.assertNotIn(participant_guardian, byes)
        # Check ambiguous, there should be one winner and one loser
        self.assertNotEqual(self.participant_fearless, ambiguous1)
        self.assertNotEqual(self.participant_valiant, ambiguous1)
        self.assertNotEqual(self.participant_victorious, ambiguous1)
        self.assertNotEqual(self.participant_invincible, ambiguous1)
        self.assertNotEqual(self.participant_dauntless, ambiguous2)
        self.assertNotEqual(self.participant_courageous, ambiguous2)
        self.assertNotEqual(self.participant_relentless, ambiguous2)
        self.assertNotEqual(self.participant_dreadnaught, ambiguous2)
        self.assertNotEqual(participant_guardian, ambiguous2)


class ModelsTest(TestCase):
    def setUp(self):
        # Create dummy players and initial event setup
        self.player_dauntless = Player.objects.create_user('dauntless@lostfleet.com', 'password')
        self.player_fearless = Player.objects.create_user('fearless@lostfleet.com', 'password')
        self.player_courageous = Player.objects.create_user('courageous@lostfleet.com', 'password')
        self.player_valiant = Player.objects.create_user('valiant@lostfleet.com', 'password')
        self.player_relentless = Player.objects.create_user('relentless@lostfleet.com', 'password')
        self.player_victorious = Player.objects.create_user('victorious@lostfleet.com', 'password')
        self.player_dreadnaught = Player.objects.create_user('dreadnaught@lostfleet.com', 'password')
        self.player_invincible = Player.objects.create_user('invincible@lostfleet.com', 'password')

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

    def test_has_received_bye(self):
        # Add another player so we have 9
        player_guardian = Player.objects.create_user('guardian@lostfleet.com', 'password')
        participant_guardian = Participant.objects.create(player=player_guardian, event=self.event)

        # Create the first round
        round1 = Round.objects.create(event=self.event)

        # Create the matches manually
        match1 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match2 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match3 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match4 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match5 = Match.objects.create(round=round1)
        ParticipantMatch.objects.create(participant=participant_guardian, match=match5, player_nr=ParticipantMatchPlayerNr.PLAYER_1)

        self.assertTrue(participant_guardian.has_received_bye())
        self.assertFalse(self.participant_invincible.has_received_bye())
        self.assertFalse(self.participant_dauntless.has_received_bye())

        # Create the second round
        round2 = Round.objects.create(event=self.event)

        # Create the matches manually
        match6 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match6, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match6, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match7 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match7, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match7, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match8 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=participant_guardian, match=match8, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match8, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match9 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match9, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match9, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match10 = Match.objects.create(round=round1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match10, player_nr=ParticipantMatchPlayerNr.PLAYER_1)

        self.assertTrue(participant_guardian.has_received_bye())
        self.assertTrue(self.participant_invincible.has_received_bye())
        self.assertFalse(self.participant_dauntless.has_received_bye())

    def test_has_played_against(self):
        # Add another player so we have 9
        player_guardian = Player.objects.create_user('guardian@lostfleet.com', 'password')
        participant_guardian = Participant.objects.create(player=player_guardian, event=self.event)

        # Create the first round
        round1 = Round.objects.create(event=self.event)

        # Create the matches manually
        match1 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match1, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match2 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match2, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match3 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match3, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match4 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match4, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match5 = Match.objects.create(round=round1)
        ParticipantMatch.objects.create(participant=participant_guardian, match=match5, player_nr=ParticipantMatchPlayerNr.PLAYER_1)

        self.assertTrue(self.participant_dauntless.has_played_against(self.participant_fearless))
        self.assertFalse(self.participant_dauntless.has_played_against(self.participant_courageous))
        self.assertFalse(self.participant_relentless.has_played_against(self.participant_dreadnaught))
        self.assertFalse(participant_guardian.has_played_against(self.participant_fearless))

        # Create the second round
        round2 = Round.objects.create(event=self.event)

        # Create the matches manually
        match6 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_dauntless, match=match6, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_courageous, match=match6, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match7 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_relentless, match=match7, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_dreadnaught, match=match7, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match8 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=participant_guardian, match=match8, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_fearless, match=match8, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match9 = Match.objects.create(round=round1, wins=2)
        ParticipantMatch.objects.create(participant=self.participant_valiant, match=match9, player_nr=ParticipantMatchPlayerNr.PLAYER_1)
        ParticipantMatch.objects.create(participant=self.participant_victorious, match=match9, player_nr=ParticipantMatchPlayerNr.PLAYER_2)
        match10 = Match.objects.create(round=round1)
        ParticipantMatch.objects.create(participant=self.participant_invincible, match=match10, player_nr=ParticipantMatchPlayerNr.PLAYER_1)

        self.assertTrue(self.participant_dauntless.has_played_against(self.participant_fearless))
        self.assertTrue(self.participant_dauntless.has_played_against(self.participant_courageous))
        self.assertTrue(self.participant_relentless.has_played_against(self.participant_dreadnaught))
        self.assertTrue(participant_guardian.has_played_against(self.participant_fearless))
