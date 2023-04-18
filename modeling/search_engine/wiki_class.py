from collections import Counter
from dataclasses import dataclass

from search_engine.analysis import analyze_
from nltk.tokenize import word_tokenize 

@dataclass
class Abstract:
    """Wikipedia abstract"""
    ID: int
    title: str
    abstract: str
    url: str

    @property
    def fulltext(self)-> str:
        return ' '.join([self.title, self.abstract])

    def analyze(self)-> None:
        self.term_frequencies = Counter(analyze_(self.fulltext))
    def term_frequency(self, term:str)->int:
        return self.term_frequencies.get(term, 0)
    def get_abs_percent(self, start:float, end:float)-> str:  # TODO: Make this cut off on words, not characters- word tokenize, then " ".join(ret_str) 
        length = len(self.abstract)
        s = 0
        e = 0
        while self.abstract[round(length*start)+s] != " ":
            s += 1
        while self.abstract[round(length*end)+e] != " ":
            e =+ 1
        ret_str = self.abstract[round(length*start)+s:round(length*end)+e]
        return ret_str
        