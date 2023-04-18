import requests
import os

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSISTENT_DIR = os.path.join(MODULE_DIR, '../../')

def download_wiki_abstracts()-> None:
    url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
    with requests.get(url, stream=True) as q:  # See below comment
        q.raise_for_status()
        wiki_dir_path = os.path.join(PERSISTENT_DIR, 'data/wiki/')
        if not os.path.exists(wiki_dir_path):
            os.mkdir(wiki_dir_path)            
        with open(os.path.join(wiki_dir_path, 'enwiki-latest-abstract.xml.gz', 'wb')) as f:
            for i, chunk in enumerate(q.iter_content(chunk_size=1000000)):  # chunking == 1 MB; repeatedly fetches from the server, thanks to above "stream=True"
                f. write(chunk)
                if i % 10 == 0:  # Print message every 10 MB?
                    print(f'Downloaded {i} megabytes', end='\r')


