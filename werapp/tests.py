from django.test import TestCase

# Create your tests here.
from django.utils.timezone import now
from werapp.enums import GameType, PairingMethod
from werapp.models import Player, MagicGame, RandomMatchesRequest, GameRound, GamePlayer
from werapp.tasks import create_random_matches


class CreateRandomMatchesTaskTest(TestCase):

    def setUp(self):
        # Create dummy players and initial game setup
        self.player_dauntless = Player.objects.create_user('dauntless', 'dauntless@lostfleet.com', 'password')
        self.player_fearless = Player.objects.create_user('fearless', 'fearless@lostfleet.com', 'password')
        self.player_courageous = Player.objects.create_user('courageous', 'courageous@lostfleet.com', 'password')
        self.player_valiant = Player.objects.create_user('valiant', 'valiant@lostfleet.com', 'password')
        self.player_relentless = Player.objects.create_user('relentless', 'relentless@lostfleet.com', 'password')
        self.player_victorious = Player.objects.create_user('victorious', 'victorious@lostfleet.com', 'password')
        self.player_dreadnaught = Player.objects.create_user('dreadnaught', 'dreadnaught@lostfleet.com', 'password')
        self.player_invincible = Player.objects.create_user('invincible', 'invincible@lostfleet.com', 'password')

        # Initial game
        self.game = MagicGame.objects.create(name='Test', date=now(), game_type=GameType.CASUAL_LIMITED,
                                             pairing_method=PairingMethod.SWISS, nr_of_rounds=3)

        # Add players as gameplayers
        self.gameplayer_dauntless = GamePlayer.objects.create(player=self.player_dauntless, magicgame=self.game)
        self.gameplayer_fearless = GamePlayer.objects.create(player=self.player_fearless, magicgame=self.game)
        self.gameplayer_courageous = GamePlayer.objects.create(player=self.player_courageous, magicgame=self.game)
        self.gameplayer_valiant = GamePlayer.objects.create(player=self.player_valiant, magicgame=self.game)
        self.gameplayer_relentless = GamePlayer.objects.create(player=self.player_relentless, magicgame=self.game)
        self.gameplayer_victorious = GamePlayer.objects.create(player=self.player_victorious, magicgame=self.game)
        self.gameplayer_dreadnaught = GamePlayer.objects.create(player=self.player_dreadnaught, magicgame=self.game)
        self.gameplayer_invincible = GamePlayer.objects.create(player=self.player_invincible, magicgame=self.game)

    def test_initial_random_matches(self):
        # Create the first round
        round = GameRound.objects.create(game=self.game)

        # Create the random matches request
        random_matches_request = RandomMatchesRequest.objects.create(round=round)

        # Run the task
        create_random_matches(random_matches_request.id)

        # Check the results
        matches = round.gamematch_set.all()
        players = []
        self.assertEqual(len(matches), 4)  # Expect 4 rounds
        for match in matches:
            for player in match.gameplayer_set.all():
                self.assertNotIn(player, players)  # Every player should be unique
                players.append(player)
        self.assertEqual(len(players), 8)  # Expect 8 players

    def test_initial_random_matches_with_bye(self):
        pass
