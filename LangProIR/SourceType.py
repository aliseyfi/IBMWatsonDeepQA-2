from enum import Enum


# Enumeration for different types of Sources
# - document: evidence based source with text derived from URL
# - query: question based source with text derived from string
class SourceType(Enum):
    document = 0
    query = 1
    passage = 2
    sentence = 3
