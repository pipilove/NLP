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

from NLP.CSA.ReadData import GlobalOptions


def test_sentences_split():
    '''
    仅仅测试句子划分是否正确，无其它作用
    '''
    with open(GlobalOptions.train_filename, encoding='utf_8_sig') as file, open(GlobalOptions.label_filename,
                                                                                encoding='utf_8_sig') as label_file:
        for (id, line), line1 in zip(enumerate(file), label_file):
            sentences = re.split(r'[。！？，!?,]|//@', line.strip().split('\t')[1])

            # if id == 9:
            print(id + 1)
            # print(sentences)
            # print(line1)
            labels = {'0': '---疑问', '1': '---否定', '2': ''}

            for sentence, label in zip(sentences, line1.strip().split(',')):
                print(sentence, labels[str(label)])

            if len(sentences) != len(line1.split(',')):
                print(id)
