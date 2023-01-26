from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from ..game.environment import Game
from ..game.agent import Player
import uuid
import time
import trio
import json

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
    request_dict = read_request(request)
    player_name = request_dict['playerName']
    killer = request_dict['killer']

    print('player name...')
    print(player_name)

    # Begin a new game
    game = Game()

    # Store the game
    game_id = str(uuid.uuid4())
    settings.HOODWINKED_GAMES[game_id] = game
    
    # Load players into the game
    api_player = Player(name=player_name, killer=killer, agent="api")
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
        'prompt': action_prompt,
        'next_request': 'action',
    }
    return JsonResponse(response_dict)

def takeAction(request):
    """
    Takes an action in the turn-based phase of the game. 
    Responds with one of the following:
        JsonResponse prompting another action
        JsonResponse indicating game over
        HttpStreamingResponse to begin a discussion

    Example URL: /action/?action_int=4&game_id=
    """

    # Get parameters from query string
    request_dict = read_request(request)
    action_int = request_dict['action_int']
    game_id = request_dict['game_id']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]

    # Store generated action in Player object
    game.store_api_action(action_int)

    # Wait until all actions have been generated
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
    """
    Takes a statement in the discussion phase of the game.


    If the discussion is ongoing, returns the rest of discussion, follow
    
    1. Log Statement in a shared discussion log that everyone can see
    2. Finish the discussion, if anyone is left
    3. Add and stream the vote prompt

    """

    # Get parameters from query string
    request_dict = read_request(request)
    game_id = request_dict['game_id']
    statement = request_dict['statement']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]

    # NOTE: Frontend has to print the API player's statement locally
    # Stream the rest of discussion and the vote prompt
    response = StreamingHttpResponse(
        game.stream_discussion(select="post", statement=statement)
    )
    response['prompt_type'] = 'vote'
    response['next_request'] = 'vote'

    return response

def makeVote(request):
    """
    1. Parse the vote
    2. Log the vote in a shared vote log that everyone can see
    3. Add and stream the vote summary
    4. Update state as necessary
    If the player was banished
        Stream that, and go to endgame internally
    If the player was not banished
        Add and stream the next action prompt
    
    
    """

    # Get parameters from query string
    request_dict = read_request(request)
    game_id = request_dict['game_id']
    vote = request_dict['vote']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]
    api_player = game.get_api_player()

    # Log vote in player.votes
    api_player.votes.append(vote)

def read_request(request):
    body_unicode = request.body.decode('utf-8')
    return dict(json.loads(body_unicode))