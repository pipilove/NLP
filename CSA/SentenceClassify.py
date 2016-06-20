#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '中文句式分析'
__time__ = '2015/11/26'
"""
import re
import itertools
import jieba


class GlobalOptions:
    train_filename = r'E:\machine_learning\NLP\data_for_user\train.csv'
    label_filename = r'E:\machine_learning\NLP\data_for_user\label_train.csv'


def ReadData():
    with open(GlobalOptions.train_filename, encoding='utf-8') as f1, open(GlobalOptions.label_filename,
                                                                          encoding='utf-8') as f2:
        trainList = [re.split(r'[。！？，!?,]|//@', line.split('\t')[1].strip()) for line in f1.readlines()]
        labelList = [line.strip().split(',') for line in f2.readlines()]
    labelList = list(itertools.chain.from_iterable(labelList))
    trainList = list(itertools.chain.from_iterable(trainList))
    return labelList, trainList


def segmentation(contentList, removeStopWords=False):
    # if removeStopWords:
    #     stopWords =
    #     ...
    wordList = []
    for content in contentList:
        segList = jieba.lcut(content)
        wordList.append(segList)
    return wordList


if __name__ == '__main__':
    labelList, trainList = ReadData()
    print(labelList[362])
    print(trainList[362])
    print(len(labelList), len(trainList))
    # wordList = segmentation(trainList)
    print("segmentation succesfully!")
