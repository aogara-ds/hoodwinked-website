from src.agent import Player
from src.environment import Game

# Define the game
game = Game()

# Load the players into the game
game.load_players([
    Player("MJ", killer=False, agent="gpt3-curie", start_location="Hallway"),
    Player("Rajveer", killer=True, agent="cli", start_location="Hallway"),
    Player("Aidan", killer=False, agent="gpt3-curie", start_location="Hallway"),
    Player("Chris", killer=False, agent="gpt3-curie", start_location="Hallway"),
    Player("Eric", killer=False, agent="gpt3-curie", start_location="Hallway"),
])

# Play the game
game.play()