import openai
import os
import torch
from dotenv import load_dotenv
from transformers import GPT2Tokenizer
from transformers.utils import logging
import time
import random
import re

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
        # # Crude rate limiting
        # time.sleep(2)

        # Ensure prompt is below 1024 tokens
        prompt = self.trim_prompt(prompt)

        # TODO: How do I want to set the model endpoint?
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

        # # Fetch response from OpenAI API
        # response = openai.Completion.create(
        #     model=model_string,
        #     prompt=self.tokenize(prompt),
        #     temperature=self.temperature,
        #     max_tokens=max_tokens,
        #     stop = stop_tokens
        # )


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

    def get_logprobs(self, prompt, max_tokens):
        # # Rate limiting options
        # # Only one ping per 2 seconds
        # time.sleep(2)

        # chat = True
        # while chat: 
        #     response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo",
        #         messages=[{'role': 'user', 'content': prompt}],
        #         temperature=self.temperature,
        #         max_tokens=8,
        #         n=10
        #     )

        #     for completion in response['choices']:
        #         completion = completion['message']['content']
        #         print(completion)
        #         nums = re.findall("[0-9]", completion)
        #         for num in nums:
        #             print(num)
        #             return int(num)
                
        # Ensure prompt is below 1024 tokens
        prompt = self.trim_prompt(prompt)

        logprobs = openai.Completion.create(
            model="text-curie-001",
            prompt=self.tokenize(prompt),
            temperature=self.temperature,
            max_tokens=max_tokens,
            logprobs=20
        )
        logprobs = logprobs['choices'][0]['logprobs']['top_logprobs'][0]
        return logprobs
    
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
    