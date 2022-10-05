import openai
import os
from dotenv import load_dotenv
from transformers import GPT2Tokenizer

class GPT3():
    def __init__(self):
        print("Configuring GPT-3")
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def tokenize(self, prompt):
        return self.tokenizer(prompt)['input_ids']
    
    def generate(self, prompt, max_tokens):
        print()
        print("The prompt for GPT3 is")
        print(prompt)
        print()
        print()

        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.tokenize(prompt),
            temperature=0.6,
            max_tokens = max_tokens
        )
        response = response['choices'][0]['text']
        response = response.replace('\n', '')
        return response
    
    def get_logprobs(self, prompt, max_tokens):
        logprobs = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.tokenize(prompt),
            temperature=1.5,
            max_tokens = max_tokens,
            logprobs = 20
        )
        logprobs = logprobs['choices'][0]['logprobs']['top_logprobs'][0]
        return logprobs
