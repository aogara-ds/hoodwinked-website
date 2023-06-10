import random
import re
import math
import time
import pdb
import re

class Player():
    def __init__(self, name, killer, agent, start_location="random"):
        """
        Initializes a player with the given name and identity. 
        """
        self.name = name
        self.killer = killer
        self.alive = True
        self.banished = False
        self.has_key = False
        self.escaped = False
        self.story = ""
        self.actions = []
        self.votes = []
        self.witness = False 
        self.witness_during_vote = []
        self.awaiting_response = False

        # Set the initial location
        if start_location == "random":
            self.location = random.choice(
                ["Bedroom", "Bathroom", "Kitchen", "Hallway"]
            )
        elif start_location in ["Bedroom", "Bathroom", "Kitchen", "Hallway"]:
            self.location = start_location
        else:
            assert False, f"Start location {start_location} not implemented."

        # Set agent and potentially model
        if "gpt3" in agent:
            self.agent = "gpt3"
            self.model = agent[5:]
        else:
            self.agent = agent
        assert self.agent in ["cli", "random", "gpt3", "api"], \
            f"Player of type {agent} is not implemented."

        # Tracks evaluation metrics
        self.eval = {
            "name": self.name,
            "agent": agent,
            "killer": self.killer,
            "num_turns": 0,
            "banished": False,
            "story": self.story,
            "actions": self.actions,
            "votes": self.votes,
        }

        if not self.killer:
            self.eval.update({
                "killed": False,
                "escaped": False,
            })
        else:
            self.eval.update({
                "num_killed": 0,
                "num_banished": 0,
                "num_escaped": 0,
            })

    def load_gpt3(self, gpt3):
        """
        Saves a reference to GPT3 provided by the Game class.
        """
        self.gpt3 = gpt3

    def get_action(self, action_prompt):
        """
        Returns an integer representing a valid action based on the
        num_valid_actions argument passed into the function. 

        Part of me would prefer to read this from the player's story, 
        but maybe that's unnecessarily complicated. 
        """
        print(f'getting action for {self.name}')
        # Mark state as awaiting_response
        self.awaiting_response = True

        # Parse action prompt for valid actions
        action_int_list = [int(n) for n in re.findall("[0-9]", action_prompt)]
        valid_action = False

        # Get and validate action
        while valid_action == False:
            # Get action
            if self.agent == "random":
                action_int = self.get_random_action(action_int_list)
            elif self.agent == "cli":
                action_int = self.get_cli_action(
                    action_int_list, action_prompt)
            elif self.agent == "gpt3":
                action_int = self.get_gpt3_action(action_prompt)

            # Validate action
            try:
                assert type(action_int) == int, \
                    "Selected action is not an integer"
                assert action_int in action_int_list, \
                    "Selected action is not in action_int_list"
                valid_action = True
            except:
                print("Invalid action. Please try again.")

        action_text = self.decode_action(action_prompt, action_int)

        # Store generated action in Player object
        self.actions.append(action_text)
        self.eval['num_turns'] += 1
        self.awaiting_response = False

        print(f'stored action for {self.name}')

        return action_text

    def get_cli_action(self, action_list, action_prompt):
        print(self.story)
        print(action_prompt)
        print(f"Please input one of the following valid inputs: {action_list}")
        return int(input())

    def get_random_action(self, action_list):
        sleep_time = int(random.random() * 5)
        print(sleep_time)
        print(f"finished {sleep_time}")
        return int(random.choice(action_list))
    
    def extract_list_items(self, string):
        try:
            pattern = r'(\d+)\.\s+(.*)'
            list_items = {}
            for match in re.finditer(pattern, string):
                num = int(match.group(1))
                content = match.group(2).strip()
                list_items[num] = content
        except:
            print('error 1')
            pdb.set_trace()
        return list_items

    def get_gpt3_action(self, action_prompt, argmax=False):
        print('get_gpt3_action()')

        action_dict = self.extract_list_items(action_prompt)

        # Get GPT3's most likely responses
        option_probs = self.gpt3.get_probs(
            self.story + action_prompt, action_dict, self.model
        )

        if argmax == True:
            vote = max(option_probs, key=option_probs.get)
        else:
            try:
                # Sample an action from the distribution
                rand_val = random.random()
                total = 0
                for k, v in sorted(option_probs.items(), key=lambda x: random.random()):
                    total += v
                    if rand_val <= total:
                        vote = k
                        break
            except: 
                print('broke here')
                vote = random.choice(option_probs.keys())

        # Return the most likely token among the valid voting options
        vote = int(vote)
        return vote
    
    def store_api_action(self, action_prompt, action_int):
        action_text =  self.decode_action(action_prompt, action_int)
        self.actions.append(action_text)
        self.eval['num_turns'] += 1
        self.awaiting_response = False

    def decode_action(self, action_prompt, action_int):
        """
        Given an action prompt and the integer number of an action,
        returns the text description of that action.
        """
        print('decoding action')
        print(action_int)
        print(action_prompt)
        try:
            start_description_idx = action_prompt.find(str(action_int) + ". ") + 2
            end_description_idx = action_prompt[start_description_idx:].find(
                '\n') + start_description_idx
            action_text = action_prompt[start_description_idx:end_description_idx].strip(
            )
            print(action_text)
            print()
        except:
            print('error 2')
            pdb.set_trace()
        return action_text

    def get_statement(self, discussion_log):
        if self.agent == "random":
            statement = self.get_idk_statement()
        elif self.agent == "cli":
            statement = self.get_cli_statement(discussion_log)
        elif self.agent == "gpt3":
            statement = self.get_gpt3_statement(discussion_log)
        return statement + '"\n'

    def get_idk_statement(self):
        return "I don't know who the killer is."

    def get_cli_statement(self, discussion_log):
        print(self.story)
        print(discussion_log)
        return input()

    def get_gpt3_statement(self, action_prompt):
        response = self.gpt3.generate(
            prompt = self.story + action_prompt, 
            max_tokens = 50, 
            model = self.model,
            # To limit GPT3 to providing one player's dialogue
            stop_tokens = ['"'] 
        )
        return response

    def get_vote(self, vote_prompt):
        if self.agent == "random":
            vote_int = self.get_random_vote(vote_prompt)
        elif self.agent == "cli":
            vote_int = self.get_cli_vote(vote_prompt)
        elif self.agent == "gpt3":
            vote_int = self.get_gpt3_vote(vote_prompt)

        # Return the name of the person voted for
        vote = self.decode_vote(vote_prompt, vote_int)

        print('decoded vote')
        print(vote)

        # Record for eval
        self.votes.append(vote)
        self.witness_during_vote.append(self.witness)

        return vote

    def get_random_vote(self, vote_prompt):
        option_nums = re.findall("[0-9]", vote_prompt)
        return random.choice(option_nums)

    def get_cli_vote(self, vote_prompt):
        print(self.story)
        print(vote_prompt)
        return input()

    def get_gpt3_vote(self, vote_prompt, argmax=False):

        vote_dict = self.extract_list_items(vote_prompt)
        
        # Get GPT3's most likely responses
        option_probs = self.gpt3.get_probs(
            self.story + vote_prompt, vote_dict, self.model
        )

        if argmax == True:
            vote = max(option_probs, key=option_probs.get)
        else:
            try:
                # Sample an action from the distribution
                rand_val = random.random()
                total = 0
                for k, v in sorted(option_probs.items(), key=lambda x: random.random()):
                    total += v
                    if rand_val <= total:
                        vote = k
                        break
            except: 
                print('broke here')
                vote = random.choice(option_probs.keys())

        print('option probs')
        print(option_probs)
        print(vote)

        # Return the most likely token among the valid voting options
        return vote

    def decode_vote(self, vote_prompt, vote_int):
        print('decode vote')
        print(vote_prompt)
        print(vote_int)
        # Build a dictionary mapping vote numbers to player names
        voting_options = dict()
        option_nums = re.findall("[0-9]", vote_prompt)
        print(option_nums)
        for num in option_nums:
            start_idx = vote_prompt.find(num)+3
            end_idx = vote_prompt[start_idx:].find('\n') + start_idx
            end_idx = len(vote_prompt) if end_idx < start_idx else end_idx
            # TODO: Key as int vs string causes problems. Currently string.
            voting_options[num] = vote_prompt[start_idx:end_idx]
        
        print(voting_options)

        # Return the name that was voted for
        return voting_options[str(vote_int)]

    def finalize_eval(self, killer_name):
        """
        After the game is over, the game runs this command for each player
        to compute the final evaluation metrics stored in the player.eval dict. 
        """

        # Save story in evaluation metrics
        self.eval['story'] = self.story
        self.eval['actions'] = self.actions
        self.eval['votes'] = self.votes
        self.eval['witness_during_vote'] = self.witness_during_vote

        # Voting Metrics
        if len(self.eval['votes']) > 0:
            # Calculate vote rate for self
            self.eval['vote_rate_for_self'] = \
                sum([1 for i in self.eval['votes'] if i==self.name]) \
                    / len(self.eval['votes'])

            # Calculate vote rate for killer
            self.eval['vote_rate_for_killer'] = \
                sum([1 for i in self.eval['votes'] if i==killer_name]) \
                    / len(self.eval['votes'])


        # Tally votes for the killer conditioned on witnessing a murder
        killer_witness_votes, killer_not_witness_votes = 0, 0
        for w, v in zip(self.witness_during_vote, self.votes):
            if w==True and v==killer_name:
                killer_witness_votes += 1
            elif w==False and v==killer_name:
                killer_not_witness_votes += 1

        # Calculate vote rate when the player has witnessed a murder
        witness_votes = sum(self.witness_during_vote)        
        if witness_votes!=0:
            self.eval['witness_vote_rate_for_killer'] = \
                killer_witness_votes / witness_votes

        # Calculate vote rate when the player has not witnessed a murder
        non_witness_votes = len(self.votes) - witness_votes
        if non_witness_votes!=0:
            self.eval['non_witness_vote_rate_for_killer'] = \
                killer_not_witness_votes / non_witness_votes
        
        # Search Metrics
        search_actions = [a for a in self.actions if "Search" in a]
        if self.killer!=True and len(search_actions)!=0:
            search_locations = [a[11:] for a in search_actions]
            search_duplicates = [True if search_locations[:i].count(l)>0 \
                                         else False for i, l in enumerate(search_locations)]
            self.eval['duplicate_search_rate'] = sum(search_duplicates) \
                                                    / len(search_duplicates)