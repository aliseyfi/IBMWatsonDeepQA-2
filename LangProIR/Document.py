from Source import *
from SourceType import *
from Passage import *
import re


# Subclass of Source - text is raw text from document
# - text: raw string from document
# - scores: list of Score objects between this document and all queries
# - passages: list of Passage objects that hold all passages from this document
class Document(Source):

    def __init__(self, text, features):
        Source.__init__(self, features, SourceType.document)
        self.text = text
        self.document_id = 0
        self.passages = self.get_passages()

    # Returns list of Passage objects and stores them in self.passages
    def get_passages(self):
        split_passages = re.split('\n\n', self.text)
        passages = []
        for paragraph in split_passages:
            passage = Passage(text=paragraph, features=self.features)
            passage.document_id = self.document_id
            passage.passage_id = len(passages)
            passages.append(passage)
        return passages

    # Returns subset of self.passages with top n scoring passages for each query
    def get_highest_passages(self, n):
        highest_passages = []
        for query_index in range(len(self.scores)):
            highest_passages.append(self.highest_passages_for_query(n, query_index))

    # Returns list of n highest scoring passages for this query
    def highest_passages_for_query(self, n, query_index):
        highest_passages = sorted(self.passages,
                                  key=lambda passage: passage.scores[query_index].weighted_score(),
                                  reverse=True)
        return highest_passages[:n]
