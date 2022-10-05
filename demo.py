from src.agent import Player
from src.environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("Regan", killer=True, agent="cli"),
    Player("Amy", killer=False, agent="gpt3"),
    Player("Spencer", killer=False, agent="gpt3"),
    Player("Lena", killer=False, agent="gpt3"),
    Player("Tim", killer=False, agent="gpt3")
])

# Play the game
game.play()