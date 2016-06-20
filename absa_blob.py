#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'LML_CH'
__time__ = '2015/12/30'

"""
from textblob import TextBlob
from textblob.np_extractors import  ConllExtractor
from ABSA.readData import ReadData

def Preprocess(Reviews):
    extractor = ConllExtractor()
    text = TextBlob(Reviews, np_extractor=extractor)
    pos = []
    sents = [sent.lower().correct() for sent in text.sentences]
    #singularize()
    #lemmatize()
    for sent in sents:
        pos.append(sent.tags)
    return text.sentences, pos, text.noun_phrases

if __name__ == "__main__":
    reviews = """my favorite features , although there are many , are the speaker phone , the radio and the infrared ."""
    sentences, pos, noun_phrase = Preprocess(reviews)
    print(sentences[0])
    print(pos)
    print(noun_phrase)