import sys
import nltk
import string
import re
import random
from nltk.corpus import wordnet

q = [[('theory',), ('scientifically', 'supportable'), ('abortion',)], [(
    'creation',), ('more', 'creation', 'better'), ('creation', 'viable'), ('torah', 'uphold')]]

#word_queries = " ".join(q)

def expand_words(words):
    ## tokenize the list of words
    templookup = words.split(" ")
    uniqueLookup = list()

    lookup = list()

    for word in templookup:
        ## for each word in the split list, create a new list which holds the synonyms
        sense_list = wordnet.synsets(word)

        if sense_list:
            i = 0
            templist = list()
            for sense in sense_list:
                templist.extend(sense_list[i].lemma_names)
                i += 1
            ## append the synonyms to the lookup list of words for the sentence
            lookup.append(templist)
        else:
            ## if there are no synonyms, append the word used as the search term
            lookup.append([word])

    # remove duplicates
    for synonyms in lookup:
        uniqueLookup.append([x for x in synonyms if x not in locals()['_[1]']])

    for x in uniqueLookup:
        print (x)
    return uniqueLookup


expand_words(q)