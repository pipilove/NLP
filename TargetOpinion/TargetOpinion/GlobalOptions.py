#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = '皮'
__mtime__ = '1/30/2016-030'
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
import os


class GlobalOptions():
    '''
    全局变量设置
    '''
    # 如果用pyinstaller转换后，a.datas中加入数据文件的路径
    patternFile = r'data/patterns.txt'
    stopwordsFile = r'data/English_stopwords.txt'
    # a.datas += Tree('TargetOpinion/Algorithm/data/', prefix='data', excludes=[''],  typecode='DATA')

    # 界面配置文件
    CONFIG_FILE_PATH = "analysis.ini"

    #界面title
    WINDOW_TITLE = "Target Opinion Analysor"
