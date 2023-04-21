import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.scrape_wikipedia_article import scrape_wikipedia_article

# fix later by changing structure of project
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
from search_engine.run_search_engine import create_wiki_index
from search_engine.wiki_class import Abstract

from agentive_functions.stop_function import stop_or_continue 
from agentive_functions.llm_functions.train import train_model
from agentive_functions.llm_functions.extract_tokens import extract_n_tokens
from agentive_functions.data_selector import next_corpus, update_log
from random import random
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--seed', type=int, default=0)
argparser.add_argument('--checkpoint', type=str, default=None)
cli_args = argparser.parse_args()

checkpoint = cli_args.checkpoint if cli_args.checkpoint != None else "gpt2"
model = AutoModelForCausalLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Set CUDA_VISIBLE_DEVICES to an empty string
# device_str = "cpu"
# device = torch.device(device_str)
# if device_str == "cpu":
#     os.environ['CUDA_VISIBLE_DEVICES'] = ''

model = model.to(device)

# Load search index object from scratch or from json; truncated, by default.
wiki_index = create_wiki_index()

loop_count = 0
did_training: bool = False
article_abs: Abstract
article: str
article_remaining: str

while True:  # infinite loop
    print(f"Loop Count: {loop_count}")
    model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)
    print(f"\n{model.device}\n")  # Verify model's device


    # Select more training data
    if did_training and not article_remaining == "":  # Check for remaining article
        did_training = False
        print(f"Continuing article: {article_abs.title} ({article_abs.ID}), {len(article_remaining)}/{len(article)} remaining.")
    else:  # Grab new article
        article, article_abs = next_corpus(wiki_index)
        article_remaining = article
        print(f"Pulling new article: {article_abs.title} ({article_abs.ID}), {len(article_remaining)}/{len(article)} remaining.")

    # Run tokenizer    
    training_tokens, training_text, article_remaining = extract_n_tokens(article_remaining, 1024, tokenizer)
    
    # Assess use of sub corpus
    probability_of_stopping = stop_or_continue(model, tokenizer, training_text, device=device)
    stop = random() < probability_of_stopping
    print(f"\nProbability of stopping: {round(probability_of_stopping, 3)}, \nStop: {stop}\n")
    
    # Train (stop == False)
    if not stop:
        mod = train_model(model, tokenizer, training_text)
        # print(mod.device)
        did_training = True
        print(f"Trained model on {len(training_text)} tokens.")

    # Update training log
    update_log(article_abs, len(article), len(article_remaining))  # default writes to .txt
    loop_count += 1