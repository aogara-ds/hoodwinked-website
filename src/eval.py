# import agent and game
import agent
import environment


results = []

for x in range(2):
    # Define the game
    game = environment.Game()

    # Load the players into the game
    game.load_players([
        agent.Player("Regan", killer=False, agent="random"),
        agent.Player("Amy", killer=True, agent="random"),
        agent.Player("Spencer", killer=False, agent="gpt3"),
        agent.Player("Lena", killer=False, agent="gpt3"),
        agent.Player("Tim", killer=False, agent="gpt3")
    ])

    # Play the game
    results.append(game.play())

print(results)
