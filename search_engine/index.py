import math
from .wiki_class import Abstract
from .timing import timing
from . import analysis
from collections import defaultdict
class Index:
    def __init__(self):
        self.index = {}  # k(type):v(type)  == token(str) : doc_ids(list[int])
        self.documents = {}  # k(type):v(type) == doc_id(int) : article_abstract(wiki_class.Abstract)
        self.log = defaultdict(int)  # k(type):v(type) == doc_id(int) : fraction_consumed(float)

    def index_document(self, document)-> None:
        if document.ID not in self.documents:
            self.documents[document.ID] = document
            document.analyze()

        for token in analysis.analyze_(document.fulltext):
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(document.ID)

    def document_frequency(self, token:str)->int:
        return len(self.index.get(token, set()))

    def inverse_document_frequency(self, token:str)-> float:
        # Manning, Hinrich and Schütze use log10, so we do too, even though it
        # doesn't really matter which log we use anyway
        # https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html
        return math.log10(len(self.documents) / self.document_frequency(token))

    def _results(self, analyzed_query:list[str])->list[any]:
        return [self.index.get(token, set()) for token in analyzed_query]

    @timing
    def search(self, query, search_type='AND', rank=False)->list[any]:
        """
        Search; this will return documents that contain words from the query,
        and rank them if requested (sets are fast, but unordered).
        Parameters:
          - query: the query string
          - search_type: ('AND', 'OR') do all query terms have to match, or just one
          - score: (True, False) if True, rank results based on TF-IDF score
        """
        if search_type not in ('AND', 'OR'):
            return []

        analyzed_query = analysis.analyze_(query)
        results = self._results(analyzed_query)
        if search_type == 'AND':
            # all tokens must be in the document
            documents = [self.documents[doc_id] for doc_id in set.intersection(*results)]
        if search_type == 'OR':
            # only one token has to be in the document
            documents = [self.documents[doc_id] for doc_id in set.union(*results)]

        if rank:
            return self.rank(analyzed_query, documents)
        return documents

    def rank(self, analyzed_query, documents):
        results = []
        if not documents:
            return results
        for document in documents:
            score = 0.0
            for token in analyzed_query:
                tf = document.term_frequency(token)
                idf = self.inverse_document_frequency(token)
                score += tf * idf
            results.append((document, score))
        return sorted(results, key=lambda doc: doc[1], reverse=True)
    
    def get__rand_doc(self, percent:float)-> Abstract:
        """ percent: float [0, 1] -> e.g. .2, .5 """

        cap = len(self.documents) 
        r_idx = (0, cap-1)  # cap-1 bc randint "includes both endpoints."
        abs_2_return = self.documents[r_idx]
        curr_perc = self.log[r_idx] % 1
        if curr_perc+percent <= 1:
            # grab the portion of the Abstract for current_perc through current_perc+percent
            # split abstract and doc into 2 different functions?? yes, allows for implementing or not that percentage function, 
            # and better abstraction of tasks
            x = 0

        self.log[randint] += percent

        return abs_2_return