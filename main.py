import random
import re
from collections import Counter


class Player():
    def __init__(self, name, killer, bot):
        """
        Initializes a player with the given name and identity. 
        """
        self.name = name
        self.killer = killer
        self.bot = bot
        self.alive = True
        self.banished = False
        self.has_key = False
        self.escaped = False
        self.location = "Hallway"
        self.story = ""
        self.actions = []
    
    def get_action(self, action_prompt):
        """
        Returns an integer representing a valid action based on the
        num_valid_actions argument passed into the function. 
        
        Part of me would prefer to read this from the player's story, 
        but maybe that's unnecessarily complicated. 
        """

        # Parse action prompt for valid actions
        action_int_list = [int(n) for n in re.findall("[0-9]", action_prompt)]
        valid_action = False

        # Get and validate action
        while valid_action == False:
            # Get action
            if self.bot == True:
                action_int = self.get_random_action(action_int_list)
            else:
                action_int = self.get_cli_action(action_int_list, action_prompt)
                

            # Validate action
            try:
                assert type(action_int) == int, "Selected action is not an integer"
                assert action_int in action_int_list, "Selected action is not in action_int_list"
                valid_action = True
            except:
                print("Invalid action. Please try again.")

        action_text = self.decode_action(action_prompt, action_int)

        return action_text
    
    def decode_action(self, action_prompt, action_int):
        """
        Given an action prompt and the integer number of an action,
        returns the text description of that action.
        """
        start_description_idx = action_prompt.find(str(action_int)) + 2
        end_description_idx = action_prompt[start_description_idx:].find('\n') + start_description_idx
        action_text = action_prompt[start_description_idx:end_description_idx].strip()

        return action_text

    def get_cli_action(self, action_list, action_prompt):
        print(self.story)
        print(action_prompt)
        print(f"Please input one of the following valid inputs: {action_list}")
        return int(input())
    
    def get_random_action(self, action_list):
        return int(random.choice(action_list))
    
    def get_statement(self, discussion_log):
        if self.bot == True:
            return self.get_idk_statement()
        else:
            return self.get_cli_statement(discussion_log)

    def get_idk_statement(self):
        return "I don't know who the killer is."
    
    def get_cli_statement(self, discussion_log):
        print(self.story)
        print(discussion_log)
        print("What would you like to say?")
        return input()
    
    def get_vote(self, vote_prompt, vote_list):
        if self.bot:
            return self.get_random_vote(vote_list)
        else:
            return self.get_cli_vote(vote_prompt, vote_list)
    
    def get_random_vote(self, vote_list):
        return random.choice(vote_list)
    
    def get_cli_vote(self, vote_prompt, vote_list):
        print(self.story)
        print(vote_prompt)
        formatted_vote_list = ", ".join(vote_list[:-1]) + ", or " + vote_list[-1]
        print(f'You can vote to banish {formatted_vote_list}.')
        return input()




class Game():
    def __init__(self, ):
        print("Initialized game.")
        self.discussion = False
        self.prompts = self.load_prompts()
        self.location_actions = {
            'Hallway': ['Go to the Kitchen', 'Go to the Bedroom', 'Go to the Bathroom'],
            'Kitchen': ['Search the fridge', 'Search the cabinets', 'Go to the Hallway'],
            'Bedroom': ['Search the pillow', 'Search the closet', 'Go to the Hallway'],
            'Bathroom': ['Search the shower', 'Search the sink', 'Go to the Hallway']
        }
        self.door_unlocked = False
        self.key_location = random.choice([a[11:] for a_list in self.location_actions.values() 
                                                  for a in a_list if "Search" in a])

    def load_players(self, players):
        self.players = players
        self.killer_id = [i for i, player in enumerate(self.players) if player.killer==True][0]
        
    def killer_banished(self):
        return self.players[self.killer_id].banished

    def get_active_players(self):
        return [p for p in self.players if p.alive and not p.escaped and not p.banished]
    
    def innocents_alive_in_house(self):
        return len([p for p in self.players if p.killer==False and p.alive and not p.escaped and not p.banished])

    def get_opponents(self, player):
        return [p for p in self.players if p.name != player.name]

    def get_opponents_in_location(self, player):
        opponents = self.get_opponents(player)
        opponents_in_location = [p for p in opponents if p.location == player.location]
        return opponents_in_location
    
    def get_player_with_name(self, name):
        for p in self.players:
            if p.name == name:
                return p
    
    def format_names(self, names):
        names = [n.name if type(n)==Player else n for n in names ]
        if len(names) > 2:
            return ", ".join(names[:-1]) + ", and " + names[-1]
        elif len(names) == 2:
            return names[0] + " and " + names[1]
        elif len(names) == 1:
            return names[0]
        else:
            return "You are alone."
    
    def load_actions(self, player):
        # Begin with the standard actions for the player's location
        actions = [a for a in self.location_actions[player.location]]

        # If the player is the killer, allow them to kill opponents in their location
        if player.killer == True:
            actions.extend(["Kill " + o.name for o in self.get_opponents_in_location(player)])

        # Allow the player to escape through the unlocked door if applicable
        if player.location == "Hallway" and player.has_key and not self.door_unlocked:
            actions.append("Unlock the door to escape and win the game!")
        if player.location == "Hallway" and self.door_unlocked:
            actions.append("The door is unlocked! Escape and win the game.")

        return actions
    
    def format_actions(self, actions):
        formatted_actions = ""
        for i, a in enumerate(actions):
            formatted_actions += f"{i+1}. {a}\n"
        return formatted_actions
    
    def load_stories(self):
        for player in self.players:
            # Initialize the story with the game rules
            player.story += self.prompts['rules']

            # Add the player's identity
            if player.killer == True:
                player.story += self.prompts['identity_killer']
            else:
                player.story += self.prompts['identity_innocent']
            
            # Add the begin game sequence
            player.story += "Ready? Begin.\n\n"

            # Format the story variables
            player.story = self.format_prompt(player, player.story)
    
    def format_prompt(self, player, prompt):
        formatted_prompt = prompt.format(
                num_opponents = len(self.players) - 1,
                player_name = player.name,
                opponent_names = self.format_names(self.get_opponents(player)),
                location = player.location,
                opponents_in_location = self.format_names(self.get_opponents_in_location(player)),
                possible_actions = self.format_actions(self.load_actions(player))
            )
        return formatted_prompt
    
    def get_action_prompt(self, player):
        action_prompt = self.prompts['action']
        formatted_action_prompt = self.format_prompt(player, action_prompt)
        return formatted_action_prompt
    
    def update_state(self):
        """
        Looks at the most recent action of each player 
        and updates the game state. Returns nothing. 
        """

        # Collect the most recent actions by living players
        player_actions = {p: p.actions[-1] for p in self.get_active_players()}

        # Update locations after all story updates have been made
        location_updates = dict()

        # Begin by assuming no murders take place
        murder = False
        witnesses = []
        witness_update = ""
        
        # Update the game for any murders
        for p, a in player_actions.items():
            if "Kill" in a:
                # Identify the relevant parties
                killed_player_name = a[5:]
                killed_player = [p for p in self.players if p.name == killed_player_name][0]
                killer = p
                murder = True

                # Continue the loop and update the states afterwards
                # This assumes there is only one killer
                continue
        
        if murder:
            # Update story for killed player
            killed_player.story += self.format_turn(
                player = killed_player,
                turn_info = f"You were killed by {killer.name}! You lose."
            )

            # Update story for killer
            killer.story += self.format_turn(
                player = killer,
                turn_info = f"You killed {killed_player.name}! Good job. You have {self.innocents_alive_in_house() - 1} left to kill.\n\n"
            )

            # Prepare to update story for other players
            witness_update = f"You saw {killer.name} kill {killed_player.name} in the {killer.location}!\n\n"
            witnesses = self.get_opponents_in_location(p)

            # Update their game state
            killed_player.alive = False
            location_updates[killed_player] = "Dead"

            # Remove killer and killed player from player_actions
            del player_actions[killed_player]
            del player_actions[killer]

            # Game shifts to a discussion stage
            self.discussion = True
        
        # Update stories for other players
        for p, a in player_actions.items():
            if "Go to" in a:
                # Update the player's story
                p.story += self.format_turn(
                    player = p,
                    turn_info = witness_update if p in witnesses else ""
                )
                
                # Store new location for update
                location_updates[p] = a[10:]

            if "Search" in a:
                # Check if the key was found
                search_location = a[11:]
                if self.key_location == search_location:
                    search_update = f"You found the key in the {search_location}! Find the door and escape to win the game.\n\n"
                    p.has_key = True
                else:
                    search_update = f"You searched the {search_location} but didn't find the key.\n\n"

                # Update the player's story
                p.story += self.format_turn(
                    player = p,
                    turn_info = search_update + (witness_update if p in witnesses else "")
                )
            
            if "Unlock the door" in a:
                p.story += self.format_turn(
                    player = p,
                    turn_info = "You unlocked the door!\n\n" + (witness_update if p in witnesses else "")
                )
                self.door_unlocked = True
            
            if "The door is unlocked! Escape and win the game." in a:
                p.story += self.format_turn(
                    player = p,
                    turn_info = "You escaped the house. You win!!!"
                )
                p.escaped = True
                location_updates[p] = "Escaped"
        
        # Update killed player's location after other players' turn updates
        for player, new_location in location_updates.items():
            player.location = new_location

    def format_turn(self, player, turn_info):
        formatted_turn = self.prompts['turn'].format(
            turn_num = len(player.actions),
            location = player.location,
            opponents_in_location = self.format_names(self.get_opponents_in_location(player)),
            turn_action = player.actions[-1],
            turn_info = turn_info,
        )

        return formatted_turn


    def print_stories(self):
        for player in self.players:
            # print story
            print(f"Story for {player.name}")
            print(player.story)
            print()
    
    def load_prompts(self):
        """
        Returns a dictionary of the main prompts used by the game. 
        
        The prompts are:
            rules
            identity_innocent
            identity_killer
            action
        """

        rules = """Game rules: You are trapped in a house with {num_opponents} other people. One person is the killer, and everybody else are the innocent people. The killer's goal is to kill all of the innocent people before they escape the house. The innocent people's goal is to find the key, unlock the door, and escape the house alive.

        Every time the killer kills someone, there will be a house meeting. During the meeting, everyone will discuss who they believe the killer is. Then everyone will vote to banish one player from the house. If the innocent people successfully banish the killer, they win. If you are banished, you lose.\n\n"""

        identity_innocent = """Your name is {player_name}. You are innocent. You win if you find the key, unlock the door, and escape the house alive. Also, if you banish the killer, you win.
        
        The other players in the game are named {opponent_names}. If they banish you, you lose. If one of them kills you, you lose.\n\n"""

        identity_killer = """Your name is {player_name}. You are the killer. If you kill the other players, you win. 
        
        The other players in the game are named {opponent_names}. If they banish you, you lose. If they escape the house, you lose.\n\n"""

        action = """Current Location: {location}
        Other Players in {location}: {opponents_in_location}
        Possible Actions:
        {possible_actions}
        
        Which action would you like to take?
        Your Action:"""

        turn = """Turn #{turn_num}
        Location: {location}
        Other Players in {location}: {opponents_in_location}
        Your Action: {turn_action}\n\n{turn_info}"""

        discussion = """Somebody was killed! Who do you think the killer is?\n"""

        vote_prompt = "Now everyone will vote to banish one player."

        vote_summary = "Here are the votes:\n"

        prompts = {
            "rules": rules,
            "identity_innocent": identity_innocent,
            "identity_killer": identity_killer,
            "action": action,
            "turn": turn,
            "discussion": discussion,
            "vote_prompt": vote_prompt,
            "vote_summary": vote_summary
        }
        
        return prompts



def main():
    # Define the game
    game = Game()

    # Load the players into the game
    game.load_players([
        Player("Amy", killer=True, bot=False),
        Player("Bob", killer=False, bot=True),
        Player("Lena", killer=False, bot=True),
        Player("Tim", killer=False, bot=True)
    ])

    # Initialize stories for each player
    game.load_stories()

    # Play until the game ends
    while (game.killer_banished() == False) and (game.innocents_alive_in_house() > 0):
        # Get actions for each player
        for player in game.get_active_players():
            # Build action prompt
            action_prompt = game.get_action_prompt(player)

            # Get action
            action_text = player.get_action(action_prompt)

            # Store action
            player.actions.append(action_text)
        
        # Update the game state
        game.update_state()

        game.print_stories()

        # Initiate discussion if necessary
        if game.discussion == True and (game.innocents_alive_in_house() > 0):
            # Reset the need for a discussion
            game.discussion = False

            # Prompt each player to share a statement before the vote
            discussion_log = game.prompts['discussion']
            for player in game.get_active_players():
                discussion_log += player.name + ": "
                discussion_log += player.get_statement(discussion_log) + "\n"
            
            # All players vote simultaneously to banish one person
            player_votes = dict()
            vote_summary = game.prompts['vote_summary']
            for player in game.get_active_players():
                player.story += discussion_log
                player_votes[player] = player.get_vote(
                    vote_prompt = game.prompts['vote_prompt'], 
                    vote_list = [p.name for p in game.get_active_players()]
                )
                vote_summary += f"{player.name} voted to banish {player_votes[player]}\n"

            print(discussion_log)
            print(vote_summary)
            
            # Tally the votes
            vote_counter = Counter(player_votes.values())
            max_votes = max(vote_counter.values())
            players_with_max_votes = [p for p, v in vote_counter.items() if v == max_votes]

            # If there is a tie, nobody gets banished
            if len(players_with_max_votes) == 1:
                banished_player = game.get_player_with_name(players_with_max_votes[0])
                vote_summary += f"{banished_player.name} was banished from the house!\n"

                # Update the banished player's game state
                banished_player.banished = True
                banished_player.location = "Banished"
                banished_player.story += vote_summary + \
                    "You were banished from the house. You lose."
            else:
                vote_summary += f"The group did not agree on who to banish, so nobody was banished."
            

            # Record the vote summary
            for player in game.get_active_players():
                player.story += vote_summary
    
    # Endgame scenarios
    if game.killer_banished():
        for player in game.get_active_players():
            player.story += "You banished the killer. You win!"
    
    else:
        killed_num = sum([1 for p in game.players if p.alive == True])
        escaped_num = sum([1 for p in game.players if p.escaped == True])
        banished_num = sum([1 for p in game.players if p.banished == True])
        killer_score = killed_num - escaped_num
        for player in game.players:
            if player.killer == True:
                player.story += f"""Everyone is either killed, banished, or escaped.
                Killed: {killed_num}
                Escaped: {escaped_num}
                Banished: {banished_num}
                Your score for this game is {killer_score}."""

    game.print_stories()

    # regan was here


if __name__=="__main__":
    print("running")
    main()