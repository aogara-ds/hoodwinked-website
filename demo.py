from src.agent import Player
from src.environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("Amy", killer=True, bot=False),
    Player("Bob", killer=False, bot=True),
    Player("Lena", killer=False, bot=True),
    Player("Tim", killer=False, bot=True)
])

# Play the game
game.play()