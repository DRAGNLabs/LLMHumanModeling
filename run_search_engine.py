import os.path
import requests

from search_engine.get_wikimedia import download_wiki_abstracts
from search_engine.build_wiki_objects import load_documents
from search_engine.timing import timing
from search_engine.index import Index

@timing
def index_documents(documents, index):
    for i, document in enumerate(documents):
        index.index_document(document)
        if i % 5000 == 0:
            print(f'Indexed {i} documents', end='\r')
    return index


if __name__ == '__main__':
    # this will only download the xml dump if you don't have a copy already;
    # just delete the file if you want a fresh copy
    if not os.path.exists('search_engine/data/wiki/enwiki-latest-abstract.xml.gz'):
        download_wiki_abstracts()

    index = index_documents(load_documents(), Index())
    print(f'Index contains {len(index.documents)} documents')

    index.search('London Beer Flood', search_type='AND')
    index.search('London Beer Flood', search_type='OR')
    index.search('London Beer Flood', search_type='AND', rank=True)
    index.search('London Beer Flood', search_type='OR', rank=True)