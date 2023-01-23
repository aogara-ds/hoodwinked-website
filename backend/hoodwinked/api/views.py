from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from ..game.environment import Game
from ..game.agent import Player
import uuid
import time
import trio

# Create your views here.
def startGame(request, bots=5):
    """
    Begins a new game of Hoodwinked by:
        Starting a game with the specified players and identities. 
        Sending asynchronous requests for the AI's first turns. 
        Storing the game in a global dictionary of all games. 
    Returns the player's first move prompt. 

    Example URL: /start/?player_name=Aidan&killer=True
    """
    # Get parameters from query string
    name = str(request.GET.get('name'))
    killer = bool(request.GET.get('killer'))

    # Begin a new game
    game = Game()

    # Store the game
    game_id = str(uuid.uuid4())
    settings.HOODWINKED_GAMES[game_id] = game
    
    # Load players into the game
    api_player = Player(name=name, killer=killer, agent="api")
    game.load_players([api_player], bots=bots)

    # Request GPT3 actions
    trio.run(game.request_bot_actions)

    # Request API action
    history, action_prompt = game.request_api_action()

    # Return the player's first prompt
    response_dict = {
        'game_id': game_id,
        'history': history,
        'prompt_type': 'action',
        'prompt': action_prompt
    }
    return JsonResponse(response_dict)

def takeAction(request):
    """
    Takes an action in the turn-based phase of the game. 
    Responses with one of the following:
        JsonResponse prompting another action
        JsonResponse indicating game over
        HttpStreamingResponse to begin a discussion

    Example URL: /action/?action_int=4&game_id=
    """

    # Get parameters from query string
    action_int = int(request.GET.get('action_int'))
    game_id = str(request.GET.get('game_id'))

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]

    # Store generated action in Player object
    game.store_api_action(action_int)

    # Wait until all responses have been generated
    start_time = time.time()
    while (time.time() - start_time) < 10:
        if game.responses_returned():
            break
        else:
            time.sleep(0.1)
    if game.responses_returned() == False:
        raise Exception('Waited more than 10 seconds for action response')
    
    # Update game state based on most recent actions
    response = game.update_state(api=True, game_id=game_id)

    return response


def makeStatement(request):



    # Respond with a vote prompt

    return None