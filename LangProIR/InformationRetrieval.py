import watson_developer_cloud

from SourceType import *
from Source import *
from Document import *
from Query import *
from Score import *
from Feature import *
from Dataset import Dataset


# Carries out entire process of Information Retrieval including
# document/query addition, analysis, and scoring
# - features: list of Feature objects used for analysis and scoring
# - queries: list of Query objects used for analysis and scoring
# - documents: list of Document objects used for analysis and scoring
class InformationRetrieval:

    def __init__(self, username, password):
        self.nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                                         username=username,
                                                                         password=password)
        self.features = []
        self.queries = []
        self.documents = []

    # Adds given list of feature names and associated weights
    # - any mismatch in name length vs. weight lengt    h assigns a weight of 0 to that feature
    # - features and weights are combined into Feature objects which are appended to the instance's feature list
    def add_features_and_weights(self, feature_names, weights):
        problem_features = []
        for feature_number, name in enumerate(feature_names):
            weight = 0
            if feature_number < len(weights):
                weight = weights[feature_number]
            feature = Feature(name, weight)
            if feature.element is not None:
                self.features.append(feature)
            else:
                problem_features.append(name)
        if len(problem_features) > 0:
            print("Problem features:")
            for feature in problem_features:
                print(feature)

    # Runs the nlu analysis on the given source
    # - possible sources are documents and queries
    # - nlu analysis is run using the instance's nlu attribute
    def analyze_source(self, source):
        return self.nlu.analyze(text=source.text, features=self.feature_elements(), language='en')

    # Adds the given source to the correct attribute list and runs appropriate analysis
    # - queries are added to the queries list
    # - documents are added to the documents list
    def add_source(self, data, kind):
        if SourceType.query == kind:
            query = Query(text=data, features=self.features)
            query.analysis = self.analyze_source(source=query)
            self.queries.append(query)

        elif SourceType.document == kind:
            document = Document(text=data, features=self.features)
            document.analysis = self.analyze_source(source=document)
            document.document_id = len(self.documents)
            self.documents.append(document)

    # Adds a query and runs analysis.
    # add_query(text) is equivalent to add_source(text, SourceType.query)
    def add_query(self, text):
        query = Query(text=text, features=self.features)
        query.analysis = self.analyze_source(source=query)
        self.queries.append(query)

    # Adds all files in the folder at the passed path as documents.
    def add_dataset(self, folder_path):
        ds = Dataset(folder_path)

        for doc in ds.get_contents():
            document = Document(text=doc, features=self.features)
            document.analysis = self.analyze_source(source=document)
            self.documents.append(document)

    # Runs entire scoring and retrieval process to return top summary sentences
    def get_summary(self, n_docs, n_passages, n_sentences):
        top_documents = self.get_top_documents(n_docs)
        top_passages = self.get_top_passages(top_documents, n_passages)
        top_sentences = self.get_top_sentences(top_passages, n_sentences)
        return top_sentences

    # Runs necessary scoring process to find top n scoring documents for each query
    # - returns 2d list (num_queries x n) of top documents for each query
    def get_top_documents(self, n):
        top_documents = []
        for document in self.documents:
            document.calculate_scores(self.queries)
        # Go through all queries
        for query_index, query in enumerate(self.queries):
            # Sort the documents by their score on this query
            query_scores = sorted(self.documents,
                                  key=lambda doc: doc.scores[query_index].weighted_score(),
                                  reverse=True)
            # Select and store the top n documents
            top_documents.append(query_scores[:n])
        return top_documents

    # Runs necessary scoring process to find top n passages from given documents for each query
    # - returns 2d list (num queries x n) of top passages for each query
    def get_top_passages(self, documents, n):
        top_passages = []
        # Go through all queries
        for query_index, query in enumerate(self.queries):
            # Get top documents for this query
            top_documents = documents[query_index]
            # List of passages from all top documents for this query
            passages = []
            # Calculate passage scores for these documents
            for document in top_documents:
                for passage in document.passages:
                    passage.analysis = self.analyze_source(passage)
                    passage.calculate_scores(self.queries)
                    passages.append(passage)
            query_scores = sorted(passages,
                                  key=lambda passage: passage.scores[query_index].weighted_score(),
                                  reverse=True)
            top_passages.append(query_scores[:n])
        return top_passages

    # Runs necessary scoring process to find top n sentences from the given passages for each query
    # - returns 2d list (num queries x n) of top sentences for each query
    def get_top_sentences(self, passages, n):
        top_sentences = []
        # Go through all queries
        for query_index, query in enumerate(self.queries):
            # Get top passages for this query
            top_passages = passages[query_index]
            # List of sentences from all top passages for this query
            sentences = []
            for passage in top_passages:
                for sentence in passage.sentences:
                    sentence.analysis = self.analyze_source(sentence)
                    sentence.calculate_scores(self.queries)
                    sentences.append(sentence)
            query_scores = sorted(sentences,
                                  key=lambda sentence: sentence.scores[query_index].weighted_score(),
                                  reverse=True)
            top_sentences.append(query_scores[:n])
        return top_sentences

    # Returns array of only the feature elements
    def feature_elements(self):
        return [feature.element for feature in self.features]

    # Returns array of only the feature names
    def feature_names(self):
        return [feature.name for feature in self.features]

    # Prints out feature scores for each query-document pairing
    def display_scores(self):
        for query_index, query in enumerate(self.queries):
            print("Query %i: %s" % (query_index, query.text))
            for document_index, score in enumerate(query.scores):
                print("\tDocument %i: %s" % (document_index, self.documents[document_index].url))
                for feature_name in score.scores:
                    print("\t\t", feature_name, score.scores[feature_name])
                print("\t\t", "total", score.total_score())
                print("\t\t", "weighted total", score.weighted_score())
