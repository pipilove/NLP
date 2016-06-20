#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'LML_CH'
__time__ = '2015/12/28'

"""


def ReadData0():
    Reviews = []
    FileName = r'data/Nokia.txt'
    # FileName = r'data/Nikon.txt'
    with open(FileName, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('[t]') or line.startswith('*') or line.startswith('\n'):
                continue  # 忽略标题
            else:  # 取出评论句子
                if (line.split("##")[1].strip()):
                    Reviews.append(line.split("##")[1].strip())

    return Reviews


def ReadData():
    Reviews = []
    for i in range(1, 2101):
        FileName = r'data/HotelReviews/comment_'
        with open(FileName + str(i) + '.txt', encoding='utf-8') as f:
            text = f.read()
            Reviews.append(text.strip())
    return Reviews
