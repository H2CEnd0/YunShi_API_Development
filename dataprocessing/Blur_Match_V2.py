# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 09:39:03 2016

@author: 何超

模糊匹配医院信息

"""
import xlrd
import difflib
import os
import re
import jieba
from xlutils.copy import copy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

global row
row = 1


def get_data():
    data = xlrd.open_workbook(r'D:\yunshidata\blur_match\unmatch_v2.xls')
    table = data.sheets()[0]  
    nrows = table.nrows
    for row in range(1,nrows):
        HCO_Province = table.cell(row,0).value
        HCOName = table.cell(row,1).value
        #通过计算获得umatch医院名与match表中相似度最大值
        HCOName_Value = compute_similarity(HCO_Province,HCOName)
        if Revise_Similarity(HCOName,HCOName_Value[2]):
            HCOName_Value.append(HCOId)
            HCOName_Value.append(HCOName)
            save_data(HCOName_Value)
            continue
        
def Revise_Similarity(Unmatch_Name,Match_Name):
    #状态码，标记两个医院是否是同一家医院    
    flag = 1    
    #匹配两个医院名字符串中的大写数字，如果同时存在数字并且不相等或者只有一个医院名有数字则说明不可能是同一家医院
    Unmatch_Upper_Digit = re.findall(r"一|二|三|四|五|六|七|八|九|十", Unmatch_Name.encode('utf-8'))
    Match_Upper_Digit = re.findall(r"一|二|三|四|五|六|七|八|九|十", Match_Name.encode('utf-8'))
    if Unmatch_Upper_Digit and Match_Upper_Digit and Unmatch_Upper_Digit !=Match_Upper_Digit:
        flag *= 0
        return flag
    if not Unmatch_Upper_Digit and Match_Upper_Digit or Unmatch_Upper_Digit and not Match_Upper_Digit:
        flag *= 0
        return flag
    #匹配两个医院名字符串中的小写数字，如果同时存在数字并且不相等或者只有一个医院名有数字则说明不可能是同一家医院
    Unmatch_Lower_Digit = re.findall(r"([\d]+)", Unmatch_Name.encode('utf-8'))
    Match_Lower_Digit = re.findall(r"([\d]+)", Match_Name.encode('utf-8'))
    if Unmatch_Lower_Digit and Match_Lower_Digit and Unmatch_Lower_Digit==Match_Lower_Digit:
        flag *= 0
        return flag
    if not Unmatch_Lower_Digit and Match_Lower_Digit or Unmatch_Lower_Digit and not Match_Lower_Digit:
        flag *= 0
        return flag
    #如果两个医院名都含有省份但是省份不相等则说明不可能是同一家医院，同理，如果两个医院名都含有市但是市不相等则说明不可能是同一家医院，如果两个医院名都含有区但是区不相等则说明不可能是同一家医院
    #利用结巴分词包，进行分词,在分词之前先将两个医院名中含有的省、市、区字去掉
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
    
     
def compute_similarity(HCO_Province,HCO_Name):
    data = xlrd.open_workbook(r'D:\yunshidata\blur_match\match_v2.xls')
    table = data.sheets()[0]  
    nrows = table.nrows
    list_dir = []
    Max_Similarity_Value = 0
    for row in range(1,nrows):
        Province_Name = table.cell(row,4).value
        if HCO_Province != Province_Name:
            continue
        HCOId = table.cell(row,0).value
        HCO_ByName = table.cell(row,1).value
        HCO_ByName1 = table.cell(row,8).value
        HCO_ByName2 = table.cell(row,10).value
        Similarity_Value = difflib.SequenceMatcher(None,HCO_ByName.encode('utf8'),Name.encode('utf8')).ratio()
        if HCO_ByName1:
            Similarity_Value1 = difflib.SequenceMatcher(None,HCO_ByName1.encode('utf8'),Name.encode('utf8')).ratio()
        else:
            Similarity_Value1 = 0
        if HCO_ByName2:
            Similarity_Value2 = difflib.SequenceMatcher(None,HCO_ByName2.encode('utf8'),Name.encode('utf8')).ratio()
        else:
            Similarity_Value2 = 0
        Value = max(Similarity_Value,Similarity_Value1,Similarity_Value2)
        if Max_Similarity_Value < Value:
            Max_Similarity_Value = Value
            list_dir = []
            list_dir.append(Max_Similarity_Value)
            list_dir.append(HCOId)
            if Value == Similarity_Value:
                list_dir.append(HCO_ByName)
                continue
            elif Value == Similarity_Value1:
                list_dir.append(HCO_ByName1)
                continue
            else:
                list_dir.append(HCO_ByName2)
                continue
    return list_dir
    
    
def save_data(list_dir):
    global row
    path = r'D:\yunshidata\blur_match\result_v2.xls'
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    sheet = wb.get_sheet(0)
    col = 0
    for td in list_dir:
        sheet.write(row,col,td)
        col +=1
    print "We Have Inserted %d Hospital Infomation Sucessfully" % row
    row+=1
    os.remove(path)
    wb.save(path)
    
    
def test():
    a= u"北京妇产医院"
    b =u"北京妇医院"
    
    similarity = difflib.SequenceMatcher(None,a.encode('utf-8'),b.encode('utf-8')).ratio()
    
    print similarity
    c = "大连理工大学"
    print '/'.join(jieba.cut(c.decode("zlib")))
    
    
if __name__ == '__main__':
    test()
    #get_data()
    '''
    query_str = "美妆 日本 Laurier花王乐而雅F系列日用护翼卫生巾（25cm*17片）瞬吸干爽超薄棉柔".decode("utf-8")  
    str_2 = "Lauríer 乐而雅 F系列敏感肌超长夜用护翼型卫生巾 40厘米 7片".decode("utf-8")#8  
    str_3 = "Lauríer 乐而雅 花王S系列超薄日用护翼卫生巾 25厘米 19片".decode("utf-8")#10  
    str_4 = "Lauríer 乐而雅 S系列 超薄瞬吸量多夜用卫生巾 30厘米 15片/包".decode("utf-8")#8  
    str_5 = "Lauríer 乐而雅 花王F系列敏感肌超量日用护翼型卫生巾 25厘米 18片".decode("utf-8")#10 
    print difflib.SequenceMatcher(None,query_str,str_2).ratio()
    print difflib.SequenceMatcher(None,query_str,str_3).ratio()
    print difflib.SequenceMatcher(None,query_str,str_4).ratio()
    print difflib.SequenceMatcher(None,query_str,str_5).ratio()
    '''