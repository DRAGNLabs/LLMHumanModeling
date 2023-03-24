import gzip
from lxml import etree  # Can't find this package; pip install lxml?
from time import time

from search_engine.wiki_class import Abstract # local .py file

def load_documents():
    start = time.time()
    # open a filehandle to the gzipped Wikipedia dump
    with gzip.open('data/enwiki.latest-abstract.xml.gz', 'rb') as f:
        doc_id = 1
        # iterparse will yield the entire `doc` element once it finds the
        # closing `</doc>` tag
        for _, element in etree.iterparse(f, events=('end',), tag='doc'):
            title = element.findtext('./title')
            url = element.findtext('./url')
            abstract = element.findtext('./abstract')

            yield Abstract(ID=doc_id, title=title, url=url, abstract=abstract)

            doc_id += 1
            # the `element.clear()` call will explicitly free up the memory
            # used to store the element
            element.clear()
    end = time.time()
    print(f'Parsing XML took {round(end - start, 3)} seconds')