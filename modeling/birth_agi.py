from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.scrape_wikipedia_article import scrape_wikipedia_article

# fix later by changing structure of project
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../')
from run_search_engine import create_wiki_index
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

model = AutoModelForCausalLM.from_pretrained(cli_args.checkpoint)
tokenizer = AutoTokenizer.from_pretrained(cli_args.checkpoint)

wiki_index = create_wiki_index()

did_training: bool = False
article_abs: Abstract
article: str
article_remaining: str

while True:
    if did_training and not article_remaining == "":
        did_training = False
    else:
        article, article_abs = next_corpus(wiki_index)
        article_remaining = article
    
    training_tokens, training_text, article_remaining = extract_n_tokens(article_remaining, 1024)
    
    probability_of_stopping = func_f(model, tokens=training_tokens)
    stop = random() < probability_of_stopping
    
    if not stop:
        train_model(model, tokenizer, training_text)
        did_training = True
    update_log(article_abs)