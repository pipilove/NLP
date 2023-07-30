#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'LML_CH'
__time__ = '2015/12/27'

"""

import nltk
from ABSA.readData import ReadData

class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences

class POSTagger(object):

    def __init__(self):
        pass

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, postag) for (word, postag) in sentence] for sentence in pos]
        return pos

def ExtactAspect(reviews):
    patternFile = r'data/patterns.txt'
    stopwordsFile = r'data/English_stopwords.txt'
    with open (stopwordsFile,encoding='utf-8')as f, open(patternFile,encoding='utf-8') as p :
        stopwords = set(line.strip() for line in f.readlines())  # 读入停用词
        P = [line.strip() for line in p.readlines()]
    # print(P)
    T = []

    for text in reviews:
        splitter = Splitter()
        postagger = POSTagger()
        splitted_sentences = splitter.split(text)
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
        for sentence in pos_tagged_sentences:
            target = 'target'
            opinion = 'opinion'
            print(sentence)
            pos = [taggedWord[2] for taggedWord in sentence]
            sentencePattern = "_"+"_".join(pos)
            # print(sentencePattern)
            for pattern in P:
                length = len(pattern.strip('_').split('_'))
                if sentencePattern.find(pattern) != -1:
                    # print(pattern)
                    index = sentencePattern.find(pattern)
                    s = sentencePattern[0:index].split('_')
                    index2 = len(s) - 1
                    for i in range(index2, index2 + length):
                        if sentence[i][2].startswith('NN'):
                            target = sentence[i][0]
                        elif sentence[i][2].startswith('JJ'):
                            opinion = sentence[i][0]
                    if target not in stopwords and opinion not in stopwords:
                        print("#####")
                        T.append(target)
                        print(target, opinion)
    return T

def result(F):
    TrueFeatureFile = r'data/true_feature_Nokia.txt'
    with open(TrueFeatureFile,encoding='utf-8') as f:
        TF = []
        for line in f.readlines():
            line.replace(', ',',')
            if ',' in line:
                tmp = line.split(',')
                for t in tmp:
                    TF.append(t.strip())
            else:
                TF.append(line.strip())
        # print (TF)
        print (len(TF))
        print (len(F))
        TP = 0
        FP = 0
        # FN = 0
        test = []
        for cf in F:
            if cf in TF:
                TP += 1
                test.append(cf)
                TF.remove(cf)
            else:
                FP += 1
        FN = len(TF)
        precision = TP/(TP+FP)
        recall = TP/(TP + FN)
        print (TP,FP,FN)
        print ('p=%f'% precision)
        print ('r=%f'% recall)
        f=(2*precision*recall)/(precision+recall)
        print ('F=%f' % f)

if __name__ == "__main__":
    # reviews = ['What can I say about this place. The staff of the restaurant is nice and the eggplant is not bad.', 'Apart from that, very uninspired food, lack of atmosphere and too expensive.','I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu.', 'Will be the last time I visit, I recommend others to avoid.','Poor quality.']
    reviews = ReadData()
    T = ExtactAspect(reviews)
    result(T)