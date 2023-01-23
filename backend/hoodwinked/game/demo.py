from agent import Player
from environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("Bob", killer=False, agent="gpt3-curie", start_location="Hallway"),
    Player("Adam", killer=True, agent="cli", start_location="Hallway"),
    Player("Jim", killer=False, agent="gpt3-curie", start_location="Hallway"),
    Player("Alice", killer=False, agent="gpt3-curie", start_location="Hallway"),
])

# Play the game
game.play()