from Score import *


# Superclass for Document and Query
# - features: list of Feature objects to use for this source
# - analysis: returned analysis from running NLU analysis
class Source:

    def __init__(self, features, source_type):
        self.features = features
        self.analysis = {}
        self.scores = []
        self.source_type = source_type

    # Calculates the relevancy score of the document with the given query and returns the score
    def relevance_score(self, query):
        # print(self.text[:20])
        score = Score(query, self, self.features, self.source_type)
        score.calculate_feature_scores()
        return score

    # Calculates relevancy score of document for all queries
    # - result is returned and stored in self.scores
    def calculate_scores(self, queries):
        scores = []
        for query in queries:
            score = self.relevance_score(query)
            # print("Query:", query.text)
            # print("Score:", score.weighted_score())
            scores.append(self.relevance_score(query))
        self.scores = scores
        return scores

