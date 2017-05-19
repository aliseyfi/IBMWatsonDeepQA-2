from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize


# Handles all scoring between query document pairs
# - query: query source that this score is for
# - document: document source that this score is for
# - features: list of feature objects to use for the scoring
# - scores: dictionary of key=feature.name, value=score
class Score:

    def __init__(self, query, source, features, source_type):
        self.query = query
        self.source = source
        self.features = features
        self.scores = {}
        self.type = source_type

    # Sums scores for all features and returns the result (this is unweighted)
    def total_score(self):
        return sum(self.scores.values())

    # Returns weighted score for all features
    def weighted_score(self):
        total_weight = sum(self.feature_weights())
        return sum([self.scores[feature.name]*feature.weight/total_weight for feature in self.features])

    # Returns array of only the feature weights
    def feature_weights(self):
        return [feature.weight for feature in self.features]

    # Calculates aggregate score for this query-document pair by individually
    # calculating the scores for each given feature
    def calculate_feature_scores(self):
        for feature in self.features:
            self.scores[feature.name] = self.calculate_score(feature)

    # Calculates score between query-document pair for the given feature
    def calculate_score(self, feature):
        query_analysis = self.query.analysis[feature.name]
        source_analysis = self.source.analysis[feature.name]
        score = 0

        for query_element in query_analysis:
            for source_element in source_analysis:
                score += self.element_score(query_element, source_element, feature, query_analysis, source_analysis)
        return score

    # Calculates score for individual elements of query-document pair analysis
    def element_score(self, query_element, document_element, feature, query_analysis, source_analysis):
        # These keys should be different for different features
        # Get document word count
        source_words = word_tokenize(self.source.text)
        if feature.name == "keywords" or feature.name == "concepts" or feature.name == "entities":
            return (query_element['relevance'] / len(query_analysis)) * \
                   (document_element['relevance']/len(source_analysis)) *\
                   Score.element_similarity(query_element, document_element, feature)
        elif feature.name == "categories":
            return query_element['score'] * document_element['score'] * Score.element_similarity(query_element,
                                                                                                 document_element,
                                                                                                 feature)

    # Calculates the similarity score between the query text and the document text
    @staticmethod
    def element_similarity(query_element, document_element, feature):
        if feature.name == "keywords" or feature.name == "concepts":
            return Score.similarity(query_element['text'], document_element['text'])
        elif feature.name == "entities":
            if 'disambiguation' in query_element.keys() and 'disambiguation' in document_element.keys():
                return Score.similarity(query_element['disambiguation']['name'],
                                        document_element['disambiguation']['name'])
            else:
                return Score.similarity(query_element['text'], document_element['text'])
        elif feature.name == "categories":
            if query_element['label'] == document_element['label']:
                return 1
            else:
                return 0

    # Calculates similarity between query and document text
    # - uses WordNet Wu and Palmer similarity score for each query-document word pairing
    @staticmethod
    def similarity(query_text, document_text):
        score = 0

        query_words = query_text.split(" ")
        document_words = document_text.split(" ")

        for query_word in query_words:
            for document_word in document_words:
                score += Score.wu_palmer_similarity(query_word, document_word)
        return score / (len(query_word)*len(document_word))

    # Converts given words into WordNet objects
    @staticmethod
    def wordnet_representation(word):
        synset = wn.synsets(word)
        if synset is None or len(synset) == 0:
            return None
        return wn.synsets(word)[0]

    # Calculates Wu and Palmer similarity for the two given raw text words
    @staticmethod
    def wu_palmer_similarity(word1, word2):
        wordnet_word1 = Score.wordnet_representation(word1)
        wordnet_word2 = Score.wordnet_representation(word2)
        if wordnet_word1 is None or wordnet_word2 is None:
            return 0
        similarity = wn.wup_similarity(wordnet_word1, wordnet_word2)
        if similarity is None:
            return 0
        return similarity
