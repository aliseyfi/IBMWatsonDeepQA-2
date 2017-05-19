from Source import *
from SourceType import *

# Subclass of Source - text derived from given text string
# - scores: list of Score objects representing the scores between
# the query and each document
# - text: string holding text for query
class Query(Source):

    def __init__(self, text, features):
        Source.__init__(self, features, SourceType.query)
        self.text = text

