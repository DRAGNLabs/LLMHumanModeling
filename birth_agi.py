from modeling.utils.scrape_wikipedia_article import scrape_wikipedia_article
from run_search_engine import create_wiki_index

wiki_index = create_wiki_index()  # Abstract object
article_abs = wiki_index.get_rand_doc()
article = scrape_wikipedia_article(article_abs.url)
print(article["body"][:100])