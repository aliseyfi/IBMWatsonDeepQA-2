#!/usr/bin/env python

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import metrics
from sklearn.svm import LinearSVC
from sklearn import datasets

'''
dev = datasets.load_files("dev")  # data import
print(dev.target_names)
dev_data_raw = dev.data
dev_label = dev.target
with open('QuestionSet.txt', 'r') as file:
    test = file.readlines()
# test = ['Is it possible for God to be timeless?']
# print(test)'''


def topic_model(train_data, train_labels, test_data):
    # ----------TFIDF--------
    vectorizer = TfidfVectorizer(
        sublinear_tf=True, max_df=0.5, stop_words='english', decode_error='ignore')
    train_data = vectorizer.fit_transform(train_data)
    test_data = vectorizer.transform(test_data)

    # ===========feature selection==========
    featureSelection = SelectKBest(score_func=chi2, k=10000)
    fit = featureSelection.fit(train_data, train_labels)
    train_data_selected = fit.transform(train_data)
    test_data_selected = fit.transform(test_data)
    print('finish selecting')

    # ===========SVM=============
    clf = OneVsRestClassifier(LinearSVC(C=0.1))
    clf.fit(train_data_selected, train_labels)
    print('finish training TFIDF')
    predicted = clf.predict(test_data_selected)

    return predicted

# print(topic_model(dev_data_raw, dev_label, test))
