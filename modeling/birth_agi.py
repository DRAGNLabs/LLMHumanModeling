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

from agentive_functions.stop_function import stop_training as func_f
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

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Set CUDA_VISIBLE_DEVICES to an empty string
device_str = "cpu"
device = torch.device(device_str)
if device_str == "cpu":
    os.environ['CUDA_VISIBLE_DEVICES'] = ''

model = model.to(device)

wiki_index = create_wiki_index()

loop_count = 0
did_training: bool = False
article_abs: Abstract
article: str
article_remaining: str

while True:
    print(f"Loop Count: {loop_count}")
    if did_training and not article_remaining == "":
        did_training = False
        print(f"Continuing article: {article_abs.title} ({article_abs.ID}), {len(article_remaining)}/{len(article)} remaining.")
    else:
        article, article_abs = next_corpus(wiki_index)
        article_remaining = article
        print(f"Pulling new article: {article_abs.title} ({article_abs.ID}), {len(article_remaining)}/{len(article)} remaining.")
        
    training_tokens, training_text, article_remaining = extract_n_tokens(article_remaining, 1024, tokenizer)
    
    probability_of_stopping = func_f(model, tokenizer, training_text, device=device)
    stop = random() < probability_of_stopping
    
    print(f"\nProbability of stopping: {round(probability_of_stopping, 3)}, \nStop: {stop}\n")
    
    if not stop:
        train_model(model, tokenizer, training_text)
        did_training = True
        print(f"Trained model on {len(training_text)} tokens.")
    update_log(article_abs, len(article), len(article_remaining))
    loop_count += 1