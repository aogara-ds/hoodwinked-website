# import agent and game
from src.agent import Player
from src.environment import Game


results = []
num_games = 20

# look into doing this dataframe style

for x in range(2):
    # Define the game
    game = Game()

    # Load the players into the game
    game.load_players([
        Player("Regan", killer=False, agent="random"),
        Player("Amy", killer=True, agent="random"),
        Player("Spencer", killer=False, agent="gpt3"),
        Player("Lena", killer=False, agent="gpt3"),
        Player("Tim", killer=False, agent="gpt3")
    ])

    # Play the game
    results.append(game.play())

print(results)


# balance between killer and innocents
# level up from killer and gpt 3
# temperature on GPT
