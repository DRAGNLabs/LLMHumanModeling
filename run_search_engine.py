# TODO: - make extraction and reinstantiation code into functions (~ln 23- ln 50)
#       - fix mutable default parameter types (tuples).
#       - Nested indices? What's going on?
#       


import json
import os.path
# import requests

from search_engine.get_wikimedia import download_wiki_abstracts
from search_engine.build_wiki_objects import load_documents
from search_engine.timing import timing
from search_engine.index import Index
from search_engine.wiki_class import Abstract
from scoping import scoping


@timing
def index_documents(documents, index: Index)-> Index:
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index


if __name__ == '__main__':
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
    if not os.path.exists('./data/wiki/truncated-enwiki-latest-abstract.xml.gz'):
        download_wiki_abstracts()

    search_index = Index()
    
    with scoping():
        raw_indexes = {}
        raw_documents = []
        if os.path.exists('./search_engine/cache/index.json') and os.path.exists('./search_engine/cache/documents.json'):  # Load existing index
            raw_indexes = json.load(open('./search_engine/cache/index.json'))
            raw_documents = json.load(open('./search_engine/cache/documents.json'))
            raw_documents = [Abstract(ID, title, abtract, url) for ID, title, abtract, url in raw_indexes]
            search_index = Index(raw_documents, raw_indexes)
        else:  # Create index
            search_index = index_documents(load_documents(), Index())

    print(f'Index contains {len(search_index.documents)} documents.')

    if not os.path.exists('./search_engine/cache'):  # Make a 'cache' directory
        os.mkdir('./search_engine/cache')

    with open('./search_engine/cache/search_index.json', 'w') as f:
        json_serializable_index = {index_str: list(set_ints) for index_str, set_ints in search_index.index.items()}
        json.dump(json_serializable_index, f, indent=4)
    with open('./search_engine/cache/documents.json', 'w') as f:
        json.dump([[doc.ID, doc.title, doc.abstract, doc.url] for doc in search_index.documents.values()], f, indent=4)

## Example searches
    # search_index.search('London Beer Flood', search_type='AND')
    # search_index.search('London Beer Flood', search_type='OR')
    # search_index.search('London Beer Flood', search_type='AND', rank=True)
    # search_index.search('London Beer Flood', search_type='OR', rank=True)