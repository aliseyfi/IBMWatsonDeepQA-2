import nltk
import os
import sys
import re
import codecs
import glob
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

def find_pos(pos_word):
    word = pos_word[0]
    pos = pos_word[1]
    verb_group = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
    noun_group = ["NN", "NNP", "NNPS", "NNS"]
    adj_groups = ["JJ", "JJR", "JJS"]
    pos_r = ["RB", "RBR", "RBS"]
    if pos in verb_group:
        return wn.VERB
    if pos in noun_group:
        return wn.NOUN
    if pos in adj_groups:
        return wn.ADJ
    if pos in pos_r:
        return wn.ADV
    else:
        return 'n'
def pos_lemmatize(inputfolder,outputfolder):
    if(os.path.exists(inputfolder)):
        os.chdir(inputfolder)
    else:
        print("ERROR!")
        return

    for file in glob.glob("*"):
        if file == os.path.basename(os.path.normpath(outputfolder)) or file=='program.py':
            continue
        f_open = codecs.open(file,"r+","utf-8",errors="ignore").readlines()
        lemmatized_file = open(os.path.join(os.path.normpath(outputfolder), file.split('.')[0]) , 'w+')

        for line in f_open:
            sentences = sent_tokenize(line)
            for sentence in sentences:
                words = sentence.split(" ")
                tokens = []
                for word in words:
                    tokens.extend(re.findall(r"[\w']+|[.,!?;:]",word))
                pos_tagged_list = nltk.pos_tag(tokens)
                wordnet_lemmatizer = WordNetLemmatizer()
                for i,word in enumerate(tokens):
                    line = str(wordnet_lemmatizer.lemmatize(word,pos=find_pos(pos_tagged_list[i])))
                    line.encode(encoding="utf-8",errors="ignore")
                    lemmatized_file.write(line.lower() + " ")
            lemmatized_file.write("\n")

def main():
    inputfolder = os.path.normpath(sys.argv[1].strip())
    outputfolder = os.path.normpath(sys.argv[2].strip())
    pos_lemmatize(inputfolder,outputfolder)



if __name__ == '__main__':
    main()