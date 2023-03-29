import requests

def download_wiki_abstracts():
    url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
    with requests.get(url, stream=True) as q:  # See below comment
        q.raise_for_status()
        with open('data/wiki/enwiki-latest-abstract.xml.gz', 'wb') as f:
            for i, chunk in enumerate(q.iter_content(chunk_size=1000000)):  # chunking == 1 MB; repeatedly fetches from the server, thanks to above "stream=True"
                f. write(chunk)
                if i % 10 == 0:  # Print message every 10 MB?
                    print(f'Downloaded {i} megabytes', end='\r')


