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
    def fulltext(self):
        return ' '.join([self.title, self.abstract])

    def analyze(self):
        self.term_frequencies = Counter(analyze_(self.fulltext)) # I added the underscore to associate it with the import, assuming it not to be recursive.

    def term_frequency(self, term):
        return self.term_frequencies.get(term, 0)