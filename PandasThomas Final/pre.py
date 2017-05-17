#!/usr/bin/env python

from sklearn import datasets
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as WLemma
from nltk.util import ngrams


with open('QuestionSet.txt', 'r') as file:
    questions = file.readlines()

puncs = set(punctuation)  # get punctuations
stops = set(stopwords.words('English'))  # get stopwords


def preprocess():
    queries = []
    for index, question in enumerate(questions):
        queries.append([])
        tokens = nltk.word_tokenize(question)
        clean_text = []
        for word in tokens:
            if word not in puncs and word not in stops:
                clean_text.append(word.lower())
        tags = nltk.pos_tag(clean_text)
        lemma_text = []
        for word in tags:
            lemma_text.append(WLemma().lemmatize(word[0]))
        for n in [1, 2, 3]:
            for ngram in ngrams(lemma_text, n):
                queries[index].append(ngram)
    return queries

# print(preprocess())
