from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from ..game.environment import Game
from ..game.agent import Player
import threading
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

    # Begin a new game
    game = Game()

    # Store the game
    game_id = str(uuid.uuid4())
    settings.HOODWINKED_GAMES[game_id] = game
    
    # Load players into the game
    api_player = Player(name=player_name, killer=killer, agent="api")
    game.load_players([api_player], bots=bots)

    print(f'btw killer is {game.get_killer().name}')

    # Request bot actions asynchronously via threads 
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

    print('takeAction')

    # Get parameters from query string
    request_dict = read_request(request)
    action_int = request_dict['input']
    game_id = request_dict['game_id']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]
    api_player = game.get_api_player()

    # Store generated action in Player object
    game.store_api_action(action_int)

    # Wait until all actions have been generated
    while (not game.threads_finished()):
        pass

    # Update game state based on most recent actions
    killed_player = game.update_state()

    # Handle the different possible outcomes
    # If someone other than the API player is killed, stream discussion
    if (killed_player != None) and (killed_player != api_player) and not game.over():
        streaming_response = StreamingHttpResponse(
            game.stream_discussion(select="pre", killed_player=killed_player)
        )
        # Set headers for streaming response
        streaming_response['game_id'] = game_id
        streaming_response['next_request'] = 'statement'

        return streaming_response

    # Request another action if the game isn't over, nobody was killed, and the API player didn't escape
    elif killed_player == None and game.over() == False and api_player.escaped == False:
        # Request GPT3 actions
        game.request_bot_actions()

        # Request API action
        history = game.request_api_action()
        next_request = 'action'
    
    elif (killed_player == api_player) or (api_player.escaped) or (game.over()):
        # Finish the rest of the game async on the server
        t = threading.Thread(target=finish_game, args=(game_id,))
        t.start()
        settings.GAME_THREADS.append(t)

        # Send the endgame message
        history = api_player.story
        next_request = 'game_over'
    
    else:
        raise Exception('Unintended outcome for takeAction.')
    
    response_dict = {
        'game_id': game_id,
        'history': history,
        'next_request': next_request,
    }

    print("here's the next action requested")
    print(next_request)

    return JsonResponse(response_dict)


def makeStatement(request):
    """
    Takes a statement in the discussion phase of the game.


    If the discussion is ongoing, returns the rest of discussion, follow
    
    1. Log Statement in a shared discussion log that everyone can see
    2. Finish the discussion, if anyone is left
    3. Add and stream the vote prompt

    """
    print('makeStatement()')

    # Get parameters from query string
    request_dict = read_request(request)
    game_id = request_dict['game_id']
    statement = request_dict['input']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]

    # Stream discussion
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
    print('makeVote()')

    # Get parameters from query string
    request_dict = read_request(request)
    game_id = request_dict['game_id']
    vote = request_dict['input']

    # Fetch stored game
    game = settings.HOODWINKED_GAMES[game_id]
    api_player = game.get_api_player()

    # Log vote in player.votes
    api_player.votes.append(vote)

    # Get the bot votes
    game.get_votes()

    # Wait for bot votes to be generated
    while (not game.threads_finished()):
        pass

    # Tally votes
    game.tally_votes()

    if game.killer_banished() or api_player.banished or api_player.escaped or game.over():
        # Finish the game
        t = threading.Thread(target=finish_game, args=(game_id,))
        t.start()
        game.threads.append(t)

        # TODO: Include endgame. This might screw up endgame on killer banished
        history = api_player.story
        next_request = 'game_over'

    # If the API player is still playing
    else:
        history = game.request_api_action()
        next_request = 'action'

    # Return message to API player
    response_dict = {
        'game_id': game_id,
        'history': history,
        'next_request': next_request,
    }

    return JsonResponse(response_dict)


def read_request(request):
    body_unicode = request.body.decode('utf-8')
    return dict(json.loads(body_unicode))

def finish_game(game_id):
    # Fetch game
    game = settings.HOODWINKED_GAMES[game_id]

    # Finish game and save results
    game.play()

    # Delete game
    settings.HOODWINKED_GAMES.pop(game_id)