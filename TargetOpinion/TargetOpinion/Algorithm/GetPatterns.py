#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'LML_CH'
__time__ = '2015/12/28'

"""
from collections import Counter
from .readData import ReadData
from .absa import Splitter, POSTagger


def FrequentAspects():
    stopwordsFile = r'data/English_stopwords.txt'
    with open(stopwordsFile, encoding='utf-8')as f:
        stopwords = set(line.strip() for line in f.readlines())  # 读入停用词
    reviews = ReadData()
    noun_counter = Counter()
    for text in reviews:
        splitter = Splitter()
        postagger = POSTagger()
        splitted_sentences = splitter.split(text)
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

        for sent in pos_tagged_sentences:
            for tagged_word in sent:
                if tagged_word[2].startswith('NN') and tagged_word[0] not in stopwords:
                    word = tagged_word[0]
                    noun_counter[word] += 1
    return [noun for noun, _ in noun_counter.most_common(20)]


def MiningPatterns(pos_tagged_sentences, KnownAspects):
    Patterns = []
    pattern = ''
    ASP_index = -1
    OP_index = -1
    distance = -1

    for sentence in pos_tagged_sentences:
        # print(sentence)
        distance = len(sentence)
        for index, tagged_word in enumerate(sentence):
            if tagged_word[1] in KnownAspects:
                ASP_index = index
                for index2, tagged_word in enumerate(sentence):
                    if tagged_word[2].startswith('JJ'):
                        # print(tagged_word[1])
                        if abs(index2 - ASP_index) < distance:
                            distance = abs(index2 - ASP_index)
                            OP_index = index2
                        # print(OP_index)
                        if OP_index < ASP_index:
                            for i in range(OP_index, ASP_index + 1):
                                pattern = pattern + '_' + sentence[i][2]
                            # pattern = pattern + '_ASP'
                            Patterns.append(pattern)
                        else:
                            for i in range(ASP_index, OP_index + 1):
                                # print(sentence[i][2])
                                pattern = pattern + '_' + sentence[i][2]
                            # pattern = "_ASP" + pattern
                            Patterns.append(pattern)
                            # print('###',sentence)

    return Patterns


def LastPatterns():
    reviews = ReadData()
    Patterns = []
    for text in reviews:
        splitter = Splitter()
        postagger = POSTagger()
        splitted_sentences = splitter.split(text)
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

        # KnownAspects = ['phone','service','ringtone','button','buttons','volume','radio','staff']  #人工设定
        # KnownAspects = ['phone', 'phones', 'nokia', 'features', 'service', 'radio', 'quality', 'speakerphone',
        # 'battery', 'screen'] #下式频率TOP10
        # KnownAspects = ['phone', 'phones', 'nokia', 'features', 'service', 'radio', 'quality', 'speakerphone',
        # 'battery', 'screen', 'sound', 'camera', 'size', 'life', 'feature', 'reception', 'voice', ')', 'excellent',
        # 't-zones']  #TOP20
        # KnownAspects = FrequentAspects()
        # print(KnownAspects)

        # KnownAspects = ['hotel','room','staff']  #人工设定
        KnownAspects = ['hotel', 'room', 'staff', 'location', 'rooms', 'service', 'Hotel', 'breakfast', 'time', 'stay',
                        'floor', 'bed', 'bathroom', 'desk', 'place', 'area', 'view', 'hotels', 'nights',
                        'price']  # TOP20

        patterns = MiningPatterns(pos_tagged_sentences, KnownAspects)
        for p in patterns:
            Patterns.append(p)
    P = [key for key, value in Counter(Patterns).items() if value > 5]  # 设置规则置信度
    return P


if __name__ == "__main__":
    P = LastPatterns()
    print(P)
    patternFile = r'data/patterns_hotel.txt'
    with open(patternFile, 'w') as f:
        for p in P:
            f.write(p + '\n')
