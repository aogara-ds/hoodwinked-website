# import agent and game
from src.agent import Player
from src.environment import Game
import time
import pandas as pd
import os

# store results in dataframe
columns = ['Game Number', 'Runtime', 'Number of Players']
eval_df = pd.DataFrame(columns=columns)

for game_num in range(20):
    # Time the game
    start_time = time.time()

    # Define the game
    game = Game()

    # Load the players into the game
    game.load_players([
        Player("Regan", killer=False, agent="random"),
        Player("Amy", killer=True, agent="random"),
        Player("Spencer", killer=False, agent="random"),
        Player("Lena", killer=False, agent="random"),
        Player("Tim", killer=False, agent="random"),
        Player("Bob", killer=False, agent="random")
    ])

    # Play the game
    player_dicts = game.play()
    end_time = time.time()

    # Store player results
    eval_df = eval_df.append(player_dicts, ignore_index=True)

    # Store game-level information
    game_idxs = eval_df.loc[eval_df.shape[0]-len(game.players):
                            eval_df.shape[0]-1].index
    eval_df.loc[game_idxs, "Game Number"] = game_num
    eval_df.loc[game_idxs, "Runtime"] = end_time - start_time
    eval_df.loc[game_idxs, "Number of Players"] = len(game.players)

# Save results as CSV
save_dir = 'results'
file_name = str(len([name for name in os.listdir(save_dir)
                if os.path.isfile(os.path.join(save_dir, name))]))
full_path = save_dir + '/' + file_name + '.csv'
eval_df.to_csv(full_path)
