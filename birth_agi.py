from modeling.utils.scrape_wikipedia_article import scrape_wikipedia_article
from run_search_engine import create_wiki_index
from modeling.agentive_functions.stop_function import stop_function as func_f


wiki_index = create_wiki_index()  # Abstract object
article_abs = wiki_index.get_rand_doc()
article = scrape_wikipedia_article(article_abs.url)
# print(article["body"][:100])  # test print

#  Func_f
func_f()