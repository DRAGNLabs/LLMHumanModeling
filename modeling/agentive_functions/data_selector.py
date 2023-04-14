from modeling.utils.scrape_wikipedia_article import scrape_wikipedia_article
from search_engine.index import Index
from search_engine.wiki_class import Abstract



def next_corpus(loaded_index : Index)-> tuple(str, Abstract):
    """Get text for random Index document. """
    article_abs = loaded_index.get_rand_doc()
    article_txt = scrape_wikipedia_article(article_abs.url)
    # print(article["body"][:100])  # test print
    return (article_txt, article_abs)

def update_log(Abs: Abstract)-> bool:
    """ Use an abstract update the log."""
    #  It worked
            #return True
    # return false