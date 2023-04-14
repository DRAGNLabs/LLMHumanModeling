from modeling.utils import scrape_wikipedia_article
from run_search_engine import do_all

abs = do_all()  # Abstract object
d = scrape_wikipedia_article(abs)
print(d["article_body"][100])
