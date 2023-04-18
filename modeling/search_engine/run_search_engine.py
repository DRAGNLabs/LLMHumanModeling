import json
import os.path
# import requests

from .get_wikimedia import download_wiki_abstracts
from .build_wiki_objects import load_documents
from .timing import timing
from .index import Index
from .wiki_class import Abstract
from scoping import scoping

PERSISTENT_DIR = '../'

@timing
def index_documents(documents, index: Index)-> Index:
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index

def create_wiki_index():
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
    if not os.path.exists(os.path.join(PERSISTENT_DIR, './data/wiki/enwiki-latest-abstract.xml.gz')):
        download_wiki_abstracts()

    search_index: Index  # Declare var for 'scoping()' funtion
    with scoping(): # Loads indexes and documents from cache if they exist, otherwise creates them
        if os.path.exists('./search_engine/cache/index.json') and os.path.exists('./search_engine/cache/documents.json'):  # Load existing index
            raw_indexes: dict = json.load(open('./search_engine/cache/index.json'))
            raw_documents: list = json.load(open('./search_engine/cache/documents.json'))
            raw_documents = [Abstract(ID, title, abtract, url) for ID, title, abtract, url in raw_documents]
            search_index = Index(raw_documents, raw_indexes)
        else:  # Create index
            search_index = index_documents(load_documents(), Index())

        print(f'Index contains {len(search_index.documents)} documents.')
        scoping.keep('search_index') # passes search_index to the enclosing scope; otherwise the variable would refer to the uninitialized Index() object.

    if not os.path.exists('./search_engine/cache/index.json') or not os.path.exists('./search_engine/cache/documents.json'):
        
        if not os.path.exists('./search_engine/cache'):  # Make a 'cache' directory
            os.mkdir('./search_engine/cache')

        # Store search_index as .json 
        with open(f'./search_engine/cache/index.json', 'w') as f:
            json_serializable_index = {index_str: list(set_ints) for index_str, set_ints in search_index.index.items()}
            json.dump(json_serializable_index, f, indent=4)
        # Store documents as .json 
        with open(f'./search_engine/cache/documents.json', 'w') as f:
            json.dump([[doc.ID, doc.title, doc.abstract, doc.url] for doc in search_index.documents.values()], f, indent=4)
    
    return search_index

## Example searches
    search_index.search('London Beer Flood', search_type='AND')
    # search_index.search('London Beer Flood', search_type='OR')
    # search_index.search('London Beer Flood', search_type='AND', rank=True)
    # search_index.search('London Beer Flood', search_type='OR', rank=True)