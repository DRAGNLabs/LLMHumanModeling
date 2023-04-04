from random import randint
from index import Index
from wiki_class import Abstract

def get_num(some_index:Index)-> int:
    cap = len(some_index.documents) 
    return randint(0, cap-1)  # cap-1 bc randint "includes both endpoints."

def log_visits(file_name:str, id:int)-> None:
    with open(f"./{file_name}.csv", mode="a", encoding="utf8") as outf:
        outf.write(id)

def get_doc(index:Index)-> Abstract:
    r_idx = get_num(some_index=index)
    log_visits(r_idx)
    abs_2_return = index.documents[r_idx]
    return abs_2_return

def clear_log(file_name:str)-> None:
    with open(f"./{file_name}.csv", mode="w", encoding="utf8") as cleanf:
        cleanf.write("File Log, Percent consumed")

