from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from ..game.environment import Game
from ..game.agent import Player
import uuid
import time
import json
import pdb


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
    player_name = request_dict['name']
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

    print('startGame requests bot actions')

    # Request bot actions asynchronously via threads 
    # TODO: Silence the warning if this is working correctly
    game.request_bot_actions()

    # Request API action
    history = game.request_api_action()

    # Return the player's first prompt
    response_dict = {
        'game_id': game_id,
        'history': history,
        'prompt_type': 'action',
        'next_request': 'action',
    }

    print('startGame finishes')

    return JsonResponse(response_dict)


def takeAction(request):
    """
    Takes an action in the turn-based phase of the game. 
    Three possible outcomes:
        If nobody is killed and the game isn't over, JsonResponse prompting another action. 
        If someone is killed, HttpStreamingResponse to begin a discussion of the killer's identity. 
        If the game is over, JsonResponse indicating game over.

    Example URL: /action/?action_int=4&game_id=
    """

    # Get parameters from query string
    request_dict = read_request(request)
    action_int = request_dict['input']
    game_id = request_dict['game_id']

    # TODO: Verify action_int is valid

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]

    # Store generated action in Player object
    game.store_api_action(action_int)

    # Wait until all actions have been generated
    while (not game.threads_finished()):
        pass

    # Update game state based on most recent actions
    killed_player = game.update_state()

    # Handle three possible followups to an action: new action, discussion, or game over
    # If nobody is killed and the game isn't over, request actions
    if killed_player == None and game.over() == False:
        # Request GPT3 actions
        game.request_bot_actions()

        # Request API action
        history = game.request_api_action()

        # Return the player's first prompt
        response_dict = {
            'game_id': game_id,
            'history': history,
            'next_request': 'action',
        }

        print('requesting action with json response')
        print(response_dict)

        return JsonResponse(response_dict)

    # If someone is killed, stream discussion
    elif killed_player != None:
        streaming_response = StreamingHttpResponse(
            game.stream_discussion(select="pre", killed_player=killed_player)
        )
        # Set headers for streaming response
        streaming_response['game_id'] = game_id
        streaming_response['next_request'] = 'vote' if \
            game.get_active_players()[-1].agent == "api" else 'statement}'
        
        print('discussion starts')
        print(streaming_response)

        return streaming_response

    # If the game is over
    elif game.over():
        # Record the endgame results
        game.endgame()

        # Give a final message to the API player
        final_message = game.killer_endgame() if game.get_api_player().killer \
            else game.prompts['innocent_victory']    

        response_dict = {
            'game_id': game_id,
            'history': history,
            'prompt': final_message,
            'next_request': 'game_over',
        }

        print('game over')
        print(response_dict)

        # TODO: Put results in the database

        return JsonResponse(response_dict)
    
    else:
        raise Exception('Unintended outcome for takeAction.')


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
    statement = request_dict['input']

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
    vote = request_dict['input']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]
    api_player = game.get_api_player()

    # Log vote in player.votes
    api_player.votes.append(vote)

def read_request(request):
    body_unicode = request.body.decode('utf-8')
    return dict(json.loads(body_unicode))