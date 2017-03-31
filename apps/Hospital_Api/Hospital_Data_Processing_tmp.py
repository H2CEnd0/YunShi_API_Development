# -*- coding: utf-8 -*-
from Connect_Mongodb import *
import xlrd
import re
import json
import difflib
import jieba
from openpyxl import load_workbook

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# 当获取到相似度最大值医院信息后,通过结巴分词再次确认是否是同一家医院
def Revise_Similarity(Unmatch_Name,Match_Name):
    print Unmatch_Name,Match_Name
    flag = 1
    Unmatch_Upper_Digit = re.findall(r"一|二|三|四|五|六|七|八|九|十", Unmatch_Name.encode('utf-8'))
    Match_Upper_Digit = re.findall(r"一|二|三|四|五|六|七|八|九|十", Match_Name.encode('utf-8'))
    if Unmatch_Upper_Digit and Match_Upper_Digit and Unmatch_Upper_Digit != Match_Upper_Digit:
        flag *= 0
        return flag
    if not Unmatch_Upper_Digit and Match_Upper_Digit or Unmatch_Upper_Digit and not Match_Upper_Digit:
        flag *= 0
        return flag
    Unmatch_Lower_Digit = re.findall(r"([\d]+)", Unmatch_Name.encode('utf-8'))
    Match_Lower_Digit = re.findall(r"([\d]+)", Match_Name.encode('utf-8'))
    if Unmatch_Lower_Digit and Match_Lower_Digit and Unmatch_Lower_Digit==Match_Lower_Digit:
        flag *= 0
        return flag
    if not Unmatch_Lower_Digit and Match_Lower_Digit or Unmatch_Lower_Digit and not Match_Lower_Digit:
        flag *= 0
        return flag
    Unmatch_Name_List = list(jieba.cut(Unmatch_Name))
    Match_Name_List = list(jieba.cut(Match_Name))
    for td in Unmatch_Name_List:
        if u'省' in td:
            for tr in Match_Name_List:
                if (u'省' in tr) and (td != tr):
                    flag *= 0
                    continue
        if u'市' in td:
            for tr in Match_Name_List:
                if (u'市' in tr) and (td != tr):
                    flag *= 0
                    continue
        if (u'区' in td) and (u'社区' not in td):
            for tr in Match_Name_List:
                if (u'区' in tr) and (u'社区' not in td) and (td != tr):
                    flag *= 0
                    continue
        if u'县' in td:
            for tr in Match_Name_List:
                if (u'县' in tr) and (td != tr):
                    flag *= 0
                    continue
        if u'镇' in td:
            for tr in Match_Name_List:
                if (u'镇' in tr) and (td != tr):
                    flag *= 0
                    continue
        if u'社区' in td:
            for tr in Match_Name_List:
                if (u'社区' in tr) and (td != tr):
                    flag *= 0
                    continue
    return flag


Revise_Similarity('上海闵行区闵联大药房','上海市人民医院')