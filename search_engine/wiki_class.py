from collections import Counter
from dataclasses import dataclass

from search_engine.analysis import analyze_

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