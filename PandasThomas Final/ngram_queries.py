import nltk
# import enchant
import string
import re
import os
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from ranking import query_rank

def getlines(path):
    f = open(path)
    lines = f.read()
    return lines

#get Tokenize
def SenToken(raws):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_tokenizer.tokenize(raws)
    return sents

#clean punctuation & digits
def cleanLines(sents):
    cleanLines = []
    #identify = string.maketrans('', '')
    for subline in sents:
        subline = re.sub('[' + string.punctuation + string.digits+ ']', "", subline)
        cleanLines.append(subline)
    return cleanLines

#Post Tagger
def POSTagger(sents):
    taggedSet = []
    for sent in sents:
        print(sent)
        taggedLine=nltk.pos_tag(nltk.word_tokenize(sent))
        taggedSet.append(taggedLine)
    return taggedSet


def WordTokener(sent):  # 将单句字符串分割成词
    wordsInStr = nltk.word_tokenize(sent)
    return wordsInStr

#n gram fuction
def word_grams(words,min,max):
    result = []
    for word in words:
        s = []
        for i in range(min, max + 1):
            #s.append(list(ngrams(word,i)))
            tmp = list(ngrams(word, i))
            if len(tmp) != 0 :
                for ngram in tmp:
                    s.append(ngram)
        result.append(s)
    #print(result)
    return result

#word extension
def expand_words (queries_expand):
    for tmp_queries in queries_expand:
        for tmp_query in tmp_queries:
            #print("tmp: " + str(tmp_query))
            if len(tmp_query) == 1:
                s = []
                for syn in wordnet.synsets(tmp_query[0]):
                    for l in syn.lemmas():
                        if (l.name(),) not in tmp_queries:
                            #print(l.name())
                            s.append((l.name(),))
        tmp_queries.extend(s)

    return queries_expand
    #print(queries_expand)



def queries_process(questionsets_path):
    english_stopwords = stopwords.words('english')

    raws = getlines(questionsets_path)
    sents = SenToken(raws)
    sents = cleanLines(sents)
    #use ngram
    #tagLine = POSTagger(sents) no use right now
    #print(tagLine)
    words = [WordTokener(cl) for cl in sents]
    #print(words)
    words = [[word.lower() for word in wordlist] for wordlist in words]
    word_filter_stopwords =[[word for word in wordlist if not word in english_stopwords] for wordlist in words]
    print(word_filter_stopwords)
    result = word_grams(word_filter_stopwords, 1, 3)
    #print(result)
    print()
    expand_queries = expand_words(result)
    #print(expand_queries)
    rank_result = query_rank(expand_queries,3)

    result_pro = [[sent +("pro",) for sent in sentlist] for sentlist in rank_result]
    #print(result_pro)
    result_con = [[sent + ('con',) for sent in sentlist] for sentlist in rank_result]
    #print(result_con)

    resultList = [result_pro,result_con]
    return resultList

