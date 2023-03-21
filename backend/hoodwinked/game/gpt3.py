import openai
import os
import torch
from dotenv import load_dotenv
from transformers import GPT2Tokenizer
from transformers.utils import logging
import time
import random
import re
import math
import numpy as np

class GPT3():
    def __init__(self, max_tokens = 16, temperature = 1):
        print("Configuring GPT-3")
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

        # Set hyperparameters
        self.max_tokens = max_tokens
        self.temperature = temperature

    def tokenize(self, prompt):
        return self.tokenizer(prompt)['input_ids']

    def generate(self, prompt, max_tokens, model, stop_tokens):
        # Ensure prompt is below 1024 tokens
        prompt = self.trim_prompt(prompt)
        
        # TODO: Flexibly support different endpoints
        # Decode model input
        model_dict = {
            "ada": "text-ada-001",
            "babbage": "text-babbage-001",
            "curie": "text-curie-001",
            "davinci-001": "text-davinci-001",
            "davinci-002": "text-davinci-002",
            "chat": "gpt-3.5-turbo"
        }
        model_string = model_dict[model]

        # Fetch response from OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{'role': 'user', 'content': prompt}],
            temperature=self.temperature,
            max_tokens=max_tokens,
            stop = stop_tokens
        )

        # Extract and clean generated text response
        response = response['choices'][0]['message']['content']
        response = response.replace('\n', '')
        return response

    def get_probs(self, prompt, action_dict, max_tokens=1, n=1, max_iters=5):

        prompt = self.trim_prompt(prompt)
        votes = {k: 0 for k in action_dict.keys()}

        print(action_dict)

        iters = 0
        while sum(votes.values()) == 0:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{'role': 'user', 'content': prompt}],
                temperature=self.temperature,
                max_tokens=max_tokens,
                n=n
            )

            for completion_dict in response['choices']:
                completion = completion_dict['message']['content']
                print(completion)
                for num, action in action_dict.items():
                    if (str(num) in completion) or (action in completion):
                        votes[num] += 1

            iters += 1
            if iters == max_iters:
                votes = {k: 1 for k in action_dict.keys()}
        
        probs = {k: np.exp(v) / sum(votes.values()) for k, v in votes.items()}

        return probs
    
    def trim_prompt(self, prompt):
        # Ignore the tokenizer warning, that's what we're fixing
        logging.set_verbosity(40)

        # While the prompt is too long, delete turns
        delete_turn_num = 0
        while len(self.tokenize(prompt)) > (1024 - self.max_tokens - 5):
            # Identify the beginning and end position of the target turn
            delete_turn_num += 1
            start_pos = prompt.find(f"Turn #{delete_turn_num}")
            end_pos = prompt.find(f"Turn #{delete_turn_num + 1}")
            prompt = prompt[:start_pos] + "...\n\n" + prompt[end_pos:]

        # Remove excess space from prompt
        excess = "...\n\n...\n\n"
        while excess in prompt:
            prompt=prompt.replace(excess,"...\n\n")
        
        return prompt
    