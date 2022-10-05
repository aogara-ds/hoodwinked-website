import random 
import re

class Player():
    def __init__(self, name, killer, agent):
        """
        Initializes a player with the given name and identity. 
        """
        self.name = name
        self.killer = killer
        self.agent = agent
        assert agent in ["cli", "random", "gpt3"], f"Player of type {agent} is not implemented."
        self.alive = True
        self.banished = False
        self.has_key = False
        self.escaped = False
        self.location = "Hallway"
        self.story = ""
        self.actions = []
    
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

        # Parse action prompt for valid actions
        action_int_list = [int(n) for n in re.findall("[0-9]", action_prompt)]
        valid_action = False

        # Get and validate action
        while valid_action == False:
            # Get action
            if self.agent == "random":
                action_int = self.get_random_action(action_int_list)
            elif self.agent == "cli":
                action_int = self.get_cli_action(action_int_list, action_prompt)
            elif self.agent == "gpt3":
                print("GPT3 actions not implemented yet")
                action_int = self.get_random_action(action_int_list)

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
        if self.agent == "random":
            return self.get_idk_statement()
        elif self.agent == "cli":
            return self.get_cli_statement(discussion_log)
        elif self.agent == "gpt3":
            return self.get_gpt3_statement(discussion_log)

    def get_idk_statement(self):
        return "I don't know who the killer is."
    
    def get_cli_statement(self, discussion_log):
        print(self.story)
        print(discussion_log)
        print("What would you like to say?")
        return input()

    def get_gpt3_statement(self, action_prompt):
        # if self.killer == False:
            # help_prompt = "Remember, you are not the killer. If you saw somebody kill somebody else, you should tell the group."        
            # action_prompt += help_prompt

        response = self.gpt3.generate(action_prompt, max_tokens = 30)
        response = response['choices'][0]['text']
        response = response.replace('\n', '')
        return response
    
    def get_vote(self, vote_prompt, vote_list):
        if self.agent == "random":
            return self.get_random_vote(vote_list)
        elif self.agent == "cli":
            return self.get_cli_vote(vote_prompt, vote_list)
        elif self.agent == "gpt3":
            print("GPT3 voting not yet implemented.")
            return self.get_random_vote(vote_list)
        
    def get_random_vote(self, vote_list):
        return random.choice(vote_list)
    
    def get_cli_vote(self, vote_prompt, vote_list):
        print(self.story)
        print(vote_prompt)
        formatted_vote_list = ", ".join(vote_list[:-1]) + ", or " + vote_list[-1]
        print(f'You can vote to banish {formatted_vote_list}.')
        return input()