#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '中文句式的句法精准分析'
__author__ = '皮'
__mtime__ = '11/26/2015-026'
__email__ = 'pipisorry@126.com'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import re
import itertools
import jieba
import numpy as np


class GlobalOptions:
    train_filename = r'E:\machine_learning\NLP\data_for_user\train.csv'
    label_filename = r'E:\machine_learning\NLP\data_for_user\label_train.csv'
    unlabeled_filename = r'E:\machine_learning\NLP\data_for_user\data.csv'

    interrogative_file = r'interrogative_sentence.txt'
    negative_file = r'negative_sentence.txt'
    declarative_file = r'declarative_sentence.txt'
    unlabeled_sentence_file = r'unlabeled_sentence.txt'

    interrogative_label = 0
    negative_label = 1
    declarative_label = 2
    class_labels = [0, 1, 2]

    unlabeled_feature_file = r'unlabeled_features.txt'
    stop_words_file = r'stop_words.txt'


def ReadData():
    with open(GlobalOptions.train_filename, encoding='utf-8') as file:
        for id, line in enumerate(file):
            sentences = re.split(r'[。！？，!?,]|//@', line.strip().split('\t')[1])
            if id == 5:
                print(sentences)
            if id >= 10:
                break
    print('************')
    with open(GlobalOptions.label_filename, encoding='utf-8') as file:
        for id, line in enumerate(file):
            if id == 5:
                print(line.strip().split(','))
                # print(len(line.split(',')))
            if id >= 10:
                break


def ClassifyData(classified_filename, label):
    '''
    将数据分类成疑问句、否定句和陈述句，分别存入文件
    '''
    with open(GlobalOptions.train_filename, encoding='utf-8') as x_file, open(GlobalOptions.label_filename,
                                                                              encoding='utf-8') as y_file:
        with open(classified_filename, 'w', encoding='utf-8') as classified_file:
            for (id, y_line), x_line in zip(enumerate(y_file), x_file):
                classified_index = np.array(y_line.strip().split(',')) == label
                # print(classified_index)

                sentences = np.array(re.split(r'[。！？，!?,]|//@', x_line.strip().split('\t')[1]))
                # print(sentences)
                classified_sentences = sentences[classified_index].tolist()
                while '' in classified_sentences:
                    classified_sentences.remove('')
                while ' ' in classified_sentences:
                    classified_sentences.remove(' ')
                # print(classified_sentences)

                if len(classified_sentences) > 0:
                    classified_file.write(('\t' + label + '\n').join(classified_sentences) + '\t' + label + '\n')


def ReadClassifiedData(classfied_file):
    '''
    从分类好的句子（文件中全是疑问或者全是否定）中读取数据
    '''
    with open(classfied_file, encoding='utf-8') as i_file:
        return [line.strip().split('\t')[0] for line in i_file]


def ReadSemiSupData(labeled_file_list, unlabeled_filename):
    '''
    读取所有文件中的数据，作为半监督学习的输入
    '''
    X = []
    Y = []
    for labeled_filename in labeled_file_list:
        with open(labeled_filename, encoding='utf-8') as labeled_file:
            for line in labeled_file:
                line_split = line.strip().split('\t')
                X.append(line_split[0:-1])
                Y.append(line_split[-1])
    labeled_no = len(Y)
    with open(unlabeled_filename, encoding='utf-8') as unlabeled_file:
        for id, line in enumerate(unlabeled_file):
            X.append(line.strip().split('\t')[0:-1])
            Y.append(-1)
            unlabeled_no = id
            # if id > 100:
            #     break
    # print(X, Y)
    Y = [int(y) for y in Y]
    return X, Y, labeled_no, unlabeled_no + 1


def ReadSemiSupDataPart(labeled_file_list, unlabeled_filename):
    '''
    读取所有文件中的数据，作为半监督学习的输入，划分数据集
    '''
    X = []
    Y = []
    unlabeled_X = []
    for labeled_filename in labeled_file_list:
        with open(labeled_filename, encoding='utf-8') as labeled_file:
            for line in labeled_file:
                line_split = line.strip().split('\t')
                X.append(line_split[0:-1])
                Y.append(line_split[-1])
    with open(unlabeled_filename, encoding='utf-8') as unlabeled_file:
        for id, line in enumerate(unlabeled_file):
            if id >= 10000000 + 400653:
                unlabeled_X.append(line.strip().split('\t')[0:-1])
                unlabeled_no = id
                # if id >= 1000 - 1:
                #     break
    # print(X, Y)
    Y = [int(y) for y in Y]
    return X, Y, unlabeled_X, unlabeled_no + 1


def ReadSupData(labeled_file_list, unlabeled_filename):
    '''
    读取所有文件中的数据，作为半监督学习的输入
    '''
    X = []
    Y = []
    unlabeled_X = []
    for labeled_filename in labeled_file_list:
        with open(labeled_filename, encoding='utf-8') as labeled_file:
            for line in labeled_file:
                line_split = line.strip().split('\t')
                X.append(line_split[0:-1])
                Y.append(line_split[-1])
    with open(unlabeled_filename, encoding='utf-8') as unlabeled_file:
        for id, line in enumerate(unlabeled_file):
            unlabeled_X.append(line.strip().split('\t')[0:-1])
            if id > 100:
                break
    # Y = [int(y) for y in Y]
    return X, Y, unlabeled_X


def PreprocessUnlabeledData():
    '''
    预处理unlabeledData
    '''
    origin_filename = GlobalOptions.unlabeled_filename
    with open(origin_filename, encoding='utf-8') as origin_file:
        # print(origin_file.readline())
        # exit()
        sentences_list = [re.split(r'[。！？，!?,]|//@', line.split('\t')[1].strip()) for line in origin_file]
        # sentences_list = re.split(r'[。！？，!?,]|//@', origin_file.readline().split('\t')[1].strip())
        # with open('line_len.txt', 'w', encoding='utf-8') as line_len_file:
        #     line_len_list = [str(len(listi)) for listi in sentences_list]
        #     line_len_file.write(' '.join(line_len_list))
        sentences_list = list(itertools.chain.from_iterable(sentences_list))

        with open(GlobalOptions.unlabeled_feature_file, 'w', encoding='utf-8') as feature_file:
            with open(GlobalOptions.stop_words_file, encoding='utf-8') as stop_file:
                stop_words_list = [line.strip() for line in stop_file]
                # print(stop_words_list)
                for content in sentences_list:
                    segList = jieba.lcut(content)
                    # for stop_word in stop_words_list:
                    #     while stop_word in segList:
                    #         segList.remove(stop_word)
                    segList = [i for i in segList if i not in stop_words_list and not re.match('\d+', i)]
                    feature_file.write('\t'.join(segList) + '\n')
                    # break


if __name__ == '__main__':
    # ReadData()

    # for filename, label in zip(
    #         [GlobalOptions.interrogative_file, GlobalOptions.negative_file, GlobalOptions.declarative_file],
    #         GlobalOptions.class_labels):
    #     ClassifyData(filename, label)

    PreprocessUnlabeledData()
