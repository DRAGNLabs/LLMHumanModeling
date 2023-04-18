import gzip
from lxml import etree  # Can't find this package; pip install lxml?
from time import time
import os

from . import wiki_class  # local .py file

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_DIR = os.path.join(MODULE_DIR, '../../')

def load_documents(truncate=True)-> wiki_class.Abstract:
    start = time()
    # open a filehandle to the gzipped Wikipedia dump
    trunc = "truncated_" if truncate else ""
    with gzip.open(os.path.join(PERSISTENT_DIR, f'./data/wiki/{trunc}enwiki-latest-abstract.xml.gz'), 'rb') as f:
        doc_id = 1
        # iterparse will yield the entire `doc` element once it finds the
        # closing `</doc>` tag
        for _, element in etree.iterparse(f, events=('end',), tag='doc'):
            title = element.findtext('./title')
            url = element.findtext('./url')
            abstract = element.findtext('./abstract')

            yield wiki_class.Abstract(ID=doc_id, title=title, url=url, abstract=abstract)

            doc_id += 1
            # the `element.clear()` call will explicitly free up the memory
            # used to store the element
            element.clear()
    end = time()
    print(f'Parsing XML took {round(end - start, 3)} seconds')