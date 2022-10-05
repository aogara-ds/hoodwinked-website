from src.agent import Player
from src.environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("Amy", killer=True, agent="cli"),
    Player("Bob", killer=False, agent="gpt3"),
    Player("Lena", killer=False, agent="gpt3"),
    Player("Tim", killer=False, agent="gpt3")
])

# Play the game
game.play()