#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '中国好创意-中文句法分析'
__author__ = '皮'
__mtime__ = '11/28/2015-028'
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
import codecs
from collections import Counter
import copy
import csv
import os
import json
import sys
import subprocess
import time
import numpy as np
from sklearn import feature_extraction, semi_supervised, svm
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error
from ReadData import ReadClassifiedData, ReadSemiSupData, ReadSupData, ReadSemiSupDataPart


class GlobalOptions():
    # uri_base = "http://ltpapi.voicecloud.cn/analysis/?"
    uri_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = "6503r3B9ZY2BIMXoESCxvNWctwVY0raflrRP8PwQ"

    interrogative_file = r'interrogative_sentence.txt'
    # interrogative_file = r'C:\Users\pi\Desktop\interrogative_sentence.txt'
    negative_file = r'negative_sentence.txt'
    declarative_file = r'declarative_sentence.txt'

    format = 'json'
    pattern = "all"
    interrogative_json_dir = r'interrogative_json'  # 疑问句法分析结果json存放目录
    neg_json_dir = r'neg_json'
    declarative_json_dir = r'declarative_json'

    tags = ['semrelate', 'pos', 'ne']
    tags_top_n = {'semrelate': 5, 'pos': 3, 'ne': 2}
    not_important_tags = {'semrelate': ['n', 'eSelt', 'mTone', 'Root'], 'pos': [], 'ne': []}
    # semrelate:语义依存分析; pos:词性标注; ne:命名实体内容
    candidate_tags_values = [{'semrelate': ['Loc', 'eSelt', 'mTone', 'Root'], 'pos': ['e', 'r', 'u'], 'ne': []},
                             {'semrelate': ['mNeg', 'eAban', 'Clas', 'eCond', 'ePref', 'Root'], 'pos': ['e', 'r', 'u'],
                              'ne': []}, {
                                 'semrelate': ['ePrec', 'eSucc', 'eProg', 'eCau', 'eResu', 'eInf', 'eSupp', 'ePurp',
                                               'eRect', 'mAux', 'mPrep', 'mRang', 'mSepa'],
                                 'pos': ['c', 'i', 'nd', 'o', 'p', 'u'], 'ne': []}]


    # format = 'plain'
    # pattern = 'all'

    interrogative_feature_file = r'interrogative_features.txt'
    negative_feature_file = r'negative_features.txt'
    declarative_feature_file = r'declarative_features.txt'
    unlabeled_feature_file = r'unlabeled_features.txt'  # 16191419行
    class_labels = [0, 1, 2]

    interrogative_feature_list_file = r'interrogative.txt'
    negative_feature_list_file = r'negative.txt'

    predict_label_file = r'predict_label.txt'
    line_len_file = r'line_len.txt'
    csv_file = r'result.csv'


def LanguageAnalysis(text, json_file):
    # if len(sys.argv) < 2 or sys.argv[1] not in ["xml", "json", "conll"]:
    #     print("usage: %s [xml/json/conll]" % sys.argv[0], file=sys.stderr)
    #     sys.exit(1)
    # Note that if your text contain special characters such as linefeed or '&', you need to use urlencode to encode
    # your data
    text = urllib.parse.quote(text)
    url = (
        GlobalOptions.uri_base + "api_key=" + GlobalOptions.api_key + "&" + "text=" + text + "&" + "format=" +
        GlobalOptions.format + "&" + "pattern=" + GlobalOptions.pattern)
    # print(url)

    try:
        if not os.path.exists(json_file):  # 已经分析过的句子不再分析！
            if not os.path.exists(os.path.dirname(json_file)):
                os.makedirs(os.path.dirname(json_file))

            response = urllib.request.urlopen(url)
            content = response.read().strip()
            # print(content.decode())

            with open(json_file, 'w', encoding='utf-8') as out_file:
                json.dump(content.decode(), out_file, indent=2)
    except urllib.error.HTTPError as e:
        print(e.reason, file=sys.stderr)


def CountTags(json_file, tag="pos"):
    '''
    从json文件中抽取并统计某个标签
    '''
    d = {}
    with open(json_file) as in_file:
        data = json.load(in_file)
        data = json.loads(data)
        for paragraph in data:
            for sentence in paragraph:
                for word in sentence:
                    pos = word[tag]
                    if pos in d:
                        d[pos] += 1
                    else:
                        d.setdefault(pos, 1)
    # print(d)
    return d


def StatFeatures(json_dir):
    '''
    对句法结构进行统计分析
    '''
    tags_sorted_dict_all = {}
    for tag in GlobalOptions.tags:
        tag_dict_list = []
        new_tag_dict = {}
        for json_file in os.listdir(json_dir):
            tag_dict = CountTags(os.path.join(json_dir, json_file), tag=tag)
            # print('tag = %s\n' % tag, tag_dict)
            tag_dict_list.append(tag_dict)
            # for key in tag_dict.keys():
            #     new_tag_dict[GlobalOptions.pos_dict[key]] = tag_dict[key]
        # print('tag = %s\n' % tag, new_tag_dict)

        # print('tag_dict_list', tag_dict_list)

        dict_vectorizer = feature_extraction.DictVectorizer()
        vectorizer_mat = dict_vectorizer.fit_transform(tag_dict_list)
        tfidf_vectorizer = feature_extraction.text.TfidfTransformer()
        tfidf_mat = tfidf_vectorizer.fit_transform(vectorizer_mat)

        col_sum_mat = np.array(tfidf_mat.sum(axis=0))
        # print(dict_vectorizer.get_feature_names())
        tags_sorted_list = np.array(dict_vectorizer.get_feature_names())[np.argsort(-col_sum_mat)[0]].tolist()
        # print(tags_sorted_list)
        # print(col_sum_mat[0][np.argsort(-col_sum_mat)[0]])
        tags_sorted_dict_all[tag] = tags_sorted_list[0:GlobalOptions.tags_top_n[tag]]
    return tags_sorted_dict_all


def BuildFeatures(json_file, tags, candidate_tags_values, id, out_file):
    '''
    从选择的features类型中选择对应的词作为features
    '''
    with open(json_file) as in_file:
        print(json_file)
        try:
            data = json.load(in_file)
            data = json.loads(data)
        except:
            return
        for paragraph in data:
            for sentence in paragraph:
                exists_flag = False
                for word in sentence:
                    for tag in tags:
                        # print(candidate_tags_values[tag])
                        if word[tag] in candidate_tags_values[tag]:
                            # print(word['cont'], word[tag], end=' ')
                            out_file.write(word['cont'] + '\t')
                            exists_flag = True
                            break
                if exists_flag:
                    out_file.write(str(GlobalOptions.class_labels[id]) + '\n')


def SemiSupClassify():
    '''
    半监督分类
    '''
    X, Y, labeled_no = ReadSemiSupData([GlobalOptions.interrogative_feature_file, GlobalOptions.negative_feature_file,
                                        GlobalOptions.declarative_feature_file], GlobalOptions.unlabeled_feature_file)
    X = [dict(Counter(x)) for x in X]
    vec = feature_extraction.DictVectorizer()
    X = vec.fit_transform(X).toarray()
    # print(X)
    # print(Y[labeled_no:])
    clf = semi_supervised.label_propagation.LabelSpreading().fit(X, Y)
    predict_label_list = [str(label) for label in clf.transduction_[labeled_no:]]
    # print(predict_label_list)
    with open(GlobalOptions.predict_label_file, 'w', encoding='utf-8') as predict_label_file:
        predict_label_file.write(' '.join(predict_label_list))


def SemiSupClassifyPart():
    '''
    半监督分类:划分test集
    '''
    X, Y, unlabeled_X, unlabeled_no = ReadSemiSupDataPart(
        [GlobalOptions.interrogative_feature_file, GlobalOptions.negative_feature_file,
         GlobalOptions.declarative_feature_file], GlobalOptions.unlabeled_feature_file)
    part_no = 4000
    part_len = unlabeled_no // part_no
    label_no = len(Y)
    Y_part = copy.deepcopy(Y)

    vec = feature_extraction.DictVectorizer()
    Y_part.extend([-1] * part_len)
    for part in range(part_no):
        with open(GlobalOptions.predict_label_file, 'a', encoding='utf-8') as predict_label_file:
            # unlabeled_X_part = unlabeled_X[part * part_len:(part + 1) * part_len]
            unlabeled_X_part = unlabeled_X[0:part_len]
            X_part = copy.deepcopy(X)
            X_part.extend(unlabeled_X_part)
            X_part = [dict(Counter(x)) for x in X_part]
            X_part = vec.fit_transform(X_part).toarray()

            clf = semi_supervised.label_propagation.LabelSpreading().fit(X_part, Y_part)
            predict_label_list = [str(label) for label in clf.transduction_[label_no:]]
            # print(predict_label_list)
            predict_label_file.write(' '.join(predict_label_list) + ' ')
            if not part % 10:
                print('part %d 完成' % part)
                # break
            unlabeled_X = unlabeled_X[part_len:]

    with open(GlobalOptions.predict_label_file, 'a', encoding='utf-8') as predict_label_file:
        remain_part = len(unlabeled_X)
        if remain_part != 0:
            X_part = copy.deepcopy(X)
            X_part.extend(unlabeled_X)
            Y_part = copy.deepcopy(Y)
            Y_part.extend([-1] * remain_part)

            X_part = [dict(Counter(x)) for x in X_part]
            X_part = vec.fit_transform(X_part).toarray()

            clf = semi_supervised.label_propagation.LabelSpreading().fit(X_part, Y_part)
            predict_label_list = [str(label) for label in clf.transduction_[label_no:]]
            # print(predict_label_list)
            predict_label_file.write(' '.join(predict_label_list) + ' ')


def GetFeaturesList(filename):
    '''
    从文件中读取features
    '''
    with open(filename, encoding='utf-8') as file:
        feature_list = [line.strip() for line in file]
    # print(feature_list)
    return feature_list


def ExtremClassify():
    '''
    基于规则的分类
    '''
    interrogative_feature_list = GetFeaturesList(GlobalOptions.interrogative_feature_list_file)
    negative_feature_list = GetFeaturesList(GlobalOptions.negative_feature_list_file)
    with open(GlobalOptions.unlabeled_feature_file, encoding='utf-8') as unlabeled_file, open(
            GlobalOptions.predict_label_file, 'w', encoding='utf-8') as predict_label_file:
        for id, line in enumerate(unlabeled_file):
            unlabeled_X = line.strip().split('\t')[0:-1]
            label = '-1'
            for i in unlabeled_X:
                if i in interrogative_feature_list:
                    label = '0'
                    break
                elif i in negative_feature_list:
                    label = '1'
                    break
            if label == '-1':
                label = '2'
            predict_label_file.write(label + ' ')
            if not id % 1000000:
                print('line %d 完成\n' % id)


def SupClassify():
    '''
    监督学习(有错)
    '''
    X, Y, unlabeled_X = ReadSupData([GlobalOptions.interrogative_feature_file, GlobalOptions.negative_feature_file,
                                     GlobalOptions.declarative_feature_file], GlobalOptions.unlabeled_feature_file)
    X = [dict(Counter(x)) for x in X]
    vec = feature_extraction.DictVectorizer()
    X = vec.fit_transform(X).toarray()
    unlabeled_X = [dict(Counter(x)) for x in unlabeled_X]
    unlabeled_X = vec.fit_transform(unlabeled_X).toarray()

    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(X, Y)

    predict_label_list = [str(label) for label in clf.predict(unlabeled_X)]
    print(predict_label_list)
    with open(GlobalOptions.predict_label_file, 'w', encoding='utf-8') as predict_label_file:
        predict_label_file.write(' '.join(predict_label_list))


def Convert2csv(line_filename, predict_label_filename, csv_filename):
    '''
    读取文件转换成提交格式的.csv文件
    '''
    with open(line_filename, encoding='utf-8') as line_file, open(csv_filename, 'w', encoding='utf-8',
                                                                  newline='') as csv_file:
        with open(predict_label_filename, encoding='utf-8') as predict_label_file:
            predict_label_list = predict_label_file.readline().strip().split()

        line_no_list = [int(i) for i in line_file.readline().strip().split()]
        # print(line_no_list[0:10])
        label_start_no = 0
        csv_w = csv.writer(csv_file, delimiter=',', lineterminator='\n')
        for line_no in line_no_list:
            csv_w.writerow(predict_label_list[label_start_no:label_start_no + line_no])
            label_start_no += line_no


if __name__ == '__main__':
    def SentencesAnalysis(infile, json_dir):
        # 读取text并进行句子级的句法分析，每个句子的句法分析结果都单独保存到json文件中
        text_list = ReadClassifiedData(infile)
        for id, text in enumerate(text_list):
            LanguageAnalysis(text, os.path.join(json_dir, str(id) + '.json'))
            if not id % 50:
                print('句子%s分析完成' % id)
                time.sleep(1)


    try:
        # SentencesAnalysis(GlobalOptions.interrogative_file, GlobalOptions.interrogative_json_dir)
        # SentencesAnalysis(GlobalOptions.negative_file, GlobalOptions.neg_json_dir)
        # SentencesAnalysis(GlobalOptions.declarative_file, GlobalOptions.declarative_json_dir)
        pass
    except Exception as e:
        print(e)
        time.sleep(1800)
        subprocess.call(['python', sys.argv[0]])


    def BuildFeaturesAll():
        tags = GlobalOptions.tags
        for id, (json_dir, feature_file) in enumerate(zip(
                [GlobalOptions.interrogative_json_dir, GlobalOptions.neg_json_dir, GlobalOptions.declarative_json_dir],
                [GlobalOptions.interrogative_feature_file, GlobalOptions.negative_feature_file,
                 GlobalOptions.declarative_feature_file])):
            if id not in [2]:
                continue
            with open(feature_file, 'w', encoding='utf-8') as out_file:
                for json_file in os.listdir(json_dir):
                    candidate_tags_values_dict = GlobalOptions.candidate_tags_values[id]
                    # candidate_tags_values_dict = StatFeatures(json_dir)
                    # print(candidate_tags_values_dict)
                    BuildFeatures(os.path.join(json_dir, json_file), tags, candidate_tags_values_dict, id, out_file)


    pass
    # BuildFeaturesAll()

    # SemiSupClassify()
    # SupClassify()
    SemiSupClassifyPart()
    # ExtremClassify()

    Convert2csv(GlobalOptions.line_len_file, GlobalOptions.predict_label_file, GlobalOptions.csv_file)
