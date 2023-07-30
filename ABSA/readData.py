#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'LML_CH'
__time__ = '2015/12/28'

"""

def ReadData():
    Reviews = []
    FileName = r'data/Nokia.txt'
    # FileName = r'data/Nikon.txt'
    with open (FileName, encoding='utf-8') as f:
        for line in f.readlines():
            if line.startswith('[t]') or line.startswith('*') or line.startswith('\n'):
                continue  # 忽略标题
            else:# 取出评论句子
                if(line.split("##")[1].strip()):
                      Reviews.append(line.split("##")[1].strip())

    return Reviews

def ReadData1():
    Reviews = []
    for i in range(1,2101):
        FileName = r'data/HotelReviews/comment_%d'

if __name__ == "__main__":
    reviews = ReadData()
    print(reviews[1])
