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
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=self.tokenize(prompt),
            temperature=0.6,
            max_tokens = max_tokens
        )
        return response











# def old_tokenize():
#     # Initalize tokenizer and labels_tokens
#     tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
#     labels = ['True', 'False']
#     labels_tokens = {label: tokenizer.encode(" " + label) for label in labels}
#     first_token_to_label = {tokens[0]: label for label, tokens in labels_tokens.items()}

# # Function for GPT3 classification query
# def classify_gpt(text, labels):ß
#     # POST Request
#     response = openai.Completion.create(
#         model="text-davinci-002",
#         prompt=generate_prompt(animal),
#         temperature=0.6
#     )

#     # Pull logprobs from response
#     top_logprobs = response["completion"]["choices"][0]["logprobs"]["top_logprobs"][0]

#     # Generate dict of token probabilities
#     token_probs = {
#         tokenizer.encode(token)[0]: np.exp(logp) 
#         for token, logp in top_logprobs.items()
#     }

#     # Generate dict of label probabilities
#     label_probs = {
#         first_token_to_label[token]: prob 
#         for token, prob in token_probs.items()
#         if token in first_token_to_label
#     }

#     # Fill in the probability for the special "Unknown" label.
#     if sum(label_probs.values()) < 1.0:
#         label_probs["Unknown"] = 1.0 - sum(label_probs.values())
    
#     return label_probs










