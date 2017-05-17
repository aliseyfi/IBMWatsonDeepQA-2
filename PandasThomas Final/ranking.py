#!/usr/bin/env python

from sklearn import datasets
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer as WLemma
from nltk.util import ngrams
from topic import topic_model

dev = datasets.load_files("train")  # data import
dev_data_raw = dev.data
dev_label = dev.target
n_class = len(dev.target_names)
# print(dev_data_raw)

puncs = set(punctuation)  # get punctuations
stops = set(stopwords.words('English'))  # get stopwords

frequency = []  # init frequencies
for i in range(n_class):
    frequency.append({})

dev_data = []
for index, line in enumerate(dev_data_raw):
    # print(line)
    line = line.decode(encoding='UTF-8', errors='ignore').split('\n')[3]
    # print('text:', line)
    tokens = nltk.word_tokenize(line)  # tokenization
    # print('tokens:', tokens)
    clean_text = []
    for word in tokens:
        if word not in puncs and word not in stops:  # remove stop words and puncs
            clean_text.append(word.lower())
    # print('remove puncs and stops:', clean_text)
    tags = nltk.pos_tag(clean_text)  # pos tag all words
    # print('POS tag:', tags)
    lemma_text = []
    for word in tags:
        lemma = WLemma().lemmatize(word[0])
        lemma_text.append(lemma)
        if (lemma,) in frequency[dev_label[index]]:
            frequency[dev_label[index]][(lemma,)] = frequency[
                dev_label[index]][(lemma,)] + 1
        else:
            frequency[dev_label[index]][(lemma,)] = 1
    # print('lemmatization:', lemma_text)
    for n in [2, 3]:  # calculate frequencies of bigrams and trigrams
        for ngram in ngrams(lemma_text, n):
            if ngram in frequency:
                frequency[dev_label[index]][ngram] = frequency[ngram] + 1
            else:
                frequency[dev_label[index]][ngram] = 1
# print('frequency:', frequency)


def query_rank(query_all, n):
    n_queries = []
    with open('QuestionSet.txt', 'r') as file:
        questions = file.readlines()
    topics = topic_model(dev_data_raw, dev_label, questions)
    print("topics: ")
    print(topics)

    for index, queries in enumerate(query_all):
        n_queries.append([])
        fre = {}
        for query in queries:
            if query in frequency[topics[index]]:
                fre[query] = frequency[topics[index]][query]
            else:
                fre[query] = 0
            idf = 0
            for f in frequency:
                if query in f:
                    idf = idf + f[query]
            fre[query] = fre[query] / (1.1 ** (idf - fre[query]))
        queries_sorted = sorted(
            fre.items(), key=lambda item: item[1], reverse=1)
        for i in range(n):
            n_queries[index].append(queries_sorted[i][0])
    return n_queries
