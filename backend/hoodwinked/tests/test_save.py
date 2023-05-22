from django.test import TestCase
from ..game.environment import Game
from ..game.environment import Player


class SaveTest(TestCase):
    def setUp(self):
        self.game = Game()
        self.game.load_players([
            Player("Bob", killer=False, agent="gpt3-curie", start_location="Hallway"),
            Player("Adam", killer=True, agent="cli", start_location="Hallway"),
            Player("Jim", killer=False, agent="gpt3-curie", start_location="Hallway"),
            Player("Alice", killer=False, agent="gpt3-curie", start_location="Hallway"),
        ])

    def test_save(self):
        self.game.endgame()

