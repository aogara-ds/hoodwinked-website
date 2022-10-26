from src.agent import Player
from src.environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("Regan", killer=False, agent="cli"),
    Player("Amy", killer=True, agent="random"),
    Player("Spencer", killer=False, agent="random"),
    Player("Lena", killer=False, agent="random"),
    Player("Tim", killer=False, agent="random")
])

# Play the game
game.play()
