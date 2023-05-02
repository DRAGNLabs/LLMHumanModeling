from utils.scrape_wikipedia_article import scrape_wikipedia_article
from search_engine.index import Index
from search_engine.wiki_class import Abstract
import csv
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_DIR = os.path.join(MODULE_DIR, '../../')

def next_corpus(loaded_index : Index)-> tuple[str, Abstract]:
    """Get text for random Index document. """
    article_abs = loaded_index.get_rand_doc()
    article_txt = scrape_wikipedia_article(article_abs.url)['body']
    # print(article["body"][:100])  # test print
    return (article_txt, article_abs)

def update_log(Abs: Abstract, len_article:int, len_read:int, to_csv:bool=False, log_id:str="")-> None:
    """ Update the log using an abstract in txt or csv.

    Optional: csv -> bool; 'True' writes out to a csv instead of txt file; default 'False'.
    Optional: log_id -> str; Add a unique id to a log (e.g. a number or model task) ; default empty str ('').
    """
    if log_id:  # Check 'type == str'and  prepend underscore
        try:
            log_id = ("_" + log_id)
        except TypeError:  # 
            log_id = "_" + str(log_id)

    travel_log_path = os.path.join(PERSISTENT_DIR, f'logs/travel_log_{log_id}')
    
    if to_csv:  # Check optional 'csv' argument == True
        file_path = travel_log_path + ".csv"

        if not os.exists(file_path):
            headers = ["File ID", "Portion", "Fraction"]
            with open(file_path, mode='w', encoding='utf8') as csv_out:
                writer = csv.writer(csv_out)
                writer.writerow(headers)

        with open(file_path, mode='a', encoding='utf8') as csv_out:
            lst_to_log = [Abs.ID, (len_read/len_article), f"{len_read}/{len_article}"]
            writer = csv.writer(csv_out)
            writer.writerow(lst_to_log)
            

    else:
        file_path = travel_log_path + ".txt"  
        with open(file_path, mode='a', encoding='utf8') as outf:
            str_to_log = f"\n File_ID: {Abs.ID}, File Used: {len_read/len_article}; ({len_read}/{len_article})." 
            outf.write(str_to_log)