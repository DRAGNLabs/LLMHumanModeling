from transformers import AutoTokenizer, AutoModelForCausalLM
from utils.scrape_wikipedia_article import scrape_wikipedia_article
from run_search_engine import create_wiki_index
from modeling.agentive_functions.stop_function import stop_training as func_f
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

while True:
    article_abs = wiki_index.get_rand_doc()
    article = scrape_wikipedia_article(wiki_index.get_rand_doc().url)
    probability_of_stopping = func_f(model, tokenizer, article)
    stop = random() < probability_of_stopping
    if not stop:
        