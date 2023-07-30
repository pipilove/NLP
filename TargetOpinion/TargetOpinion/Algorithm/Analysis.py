#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import nltk
import sys
from textblob import TextBlob

from NLP.TargetOpinion.TargetOpinion.GlobalOptions import GlobalOptions


class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def sentence(self, text):
        sentences = self.nltk_splitter.tokenize(text)
        return sentences

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        # sentences = self.nltk_splitter.tokenize(text)
        sentences = re.split(r'[.!?]', text)
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
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence',
            ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one',
                    ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, postag) for (word, postag) in sentence] for sentence in pos]
        return pos


def ExtactAspect(text):
    if getattr(sys, 'frozen', False):
        pathname = sys._MEIPASS
    else:
        pathname = os.path.split(os.path.realpath(__file__))[0]
    # print("pathname: " + pathname)

    patternFile = GlobalOptions.patternFile
    stopwordsFile = GlobalOptions.stopwordsFile
    patternFile = os.path.join(pathname, patternFile)
    stopwordsFile = os.path.join(pathname, stopwordsFile)

    with open(stopwordsFile, encoding='utf-8')as f, open(patternFile, encoding='utf-8') as p:
        stopwords = set(line.strip() for line in f.readlines())  # 读入停用词
        P = [line.strip() for line in p.readlines()]
    # print(P)
    T = []
    splitter = Splitter()
    postagger = POSTagger()
    splitted_sentences = splitter.split(text)
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    for sentence in pos_tagged_sentences:
        t = []
        target = 'target'
        opinion = 'opinion'
        # print(sentence)
        pos = [taggedWord[2] for taggedWord in sentence]
        sentencePattern = "_" + "_".join(pos)
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
                    # print("#####")
                    t.append((target, opinion))
                    # print(target, opinion)

        T.append(t)
    return T


def analysis(self, text):
    result = ExtactAspect(text)
    splitter = Splitter()
    sentences = splitter.sentence(text)
    return [str(sent) for sent in sentences], [str(r) for r in result], [str(TextBlob(sent).sentiment.polarity) for sent
                                                                         in sentences]
