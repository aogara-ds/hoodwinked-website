import os
import pandas as pd
import time
from src.environment import Game
from src.agent import Player
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_save_path():
    """
    Returns a pathname to be used throughout the evaluation. 
    """
    save_dir = 'results'
    file_name = str(len([name for name in os.listdir(save_dir)
                    if os.path.isfile(os.path.join(save_dir, name))]))
    full_path = save_dir + '/' + file_name + '.csv'
    return full_path

# Prepare DataFrame to store results
columns = ['Game Number', "Setup", 'Runtime',
           'Number of Players', 'Discussion']
eval_df = pd.DataFrame(columns=columns)
save_path = get_save_path()

# Run a number of games
for game_num in range(1000):
    # Time the game
    start_time = time.time()

    # Define the game
    discussion = (game_num % 2 == 0)
    game = Game(discussion=discussion)

    # Load the players into the game
    game.load_players([
        Player("Regan", killer=False, agent="gpt3"),
        Player("Amy", killer=True, agent="gpt3"),
        Player("Spencer", killer=False, agent="gpt3"),
        Player("Lena", killer=False, agent="gpt3"),
        Player("Tim", killer=False, agent="gpt3"),
        Player("Bob", killer=False, agent="gpt3")
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
    eval_df.loc[game_idxs, "Setup"] = "all_gpt"
    eval_df.loc[game_idxs, "Runtime"] = end_time - start_time
    eval_df.loc[game_idxs, "Number of Players"] = len(game.players)
    eval_df.loc[game_idxs, "Discussion"] = discussion

    # Save results every 50 games
    if game_num % 20 == 0:
        print(f"Saving first {game_num} games")
        eval_df.to_csv(save_path)

# Save results as CSV
eval_df.to_csv(save_path)