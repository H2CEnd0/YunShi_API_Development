# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:00:53 2016

@author: FC-05
"""

from pymongo import MongoClient
import xlrd
from xlutils.copy import copy
import os
import pymssql

server = r'192.168.7.81'
user = r'sa'
password = r'A136668132'
sql_name = r'XMasterData'
global conn
conn = pymssql.connect(server,user, password,sql_name,charset="utf8") 

'''
conn = MongoClient("115.28.77.178",27017)
global db
db = conn.country_lunwen2
'''

def get_data():
    posts = db['zhongnandaxue']
    print posts.count({})
    for td in posts.find({}):
        list_dir = []
        list_dir.append(str(td['_id']))
        list_dir.append(td[u'作者名字'])
        list_dir.append(td[u'论文名字'])
        save_data(list_dir)
        
        
def save_data(data,row):
    path = r'D:\yunshidata\Hospital_Data_Processing\1718.xls'
    rb = xlrd.open_workbook(path)
    wb = copy(rb)
    sheet = wb.get_sheet(0)
    sheet.write(row,5,data)
    print "We Have Inserted %d Hospital Infomation Sucessfully" % row
    os.remove(path)
    wb.save(path)
    
    
def connect_sqlserver(hospital_name):
    cursor = conn.cursor(as_dict=True) 
    cursor.execute("select a.HCO_Name,b.MedicalOrgName from dbo.Test a,dbo.Medical_Org_All b where b.MedicalOrgName like ('%'+cast(a.HCO_Name as varchar)+'%');")
    list_dir =[]
    for td in cursor:
        list_dir.append(str(td))
    return list_dir
    
    
def blur_match():
    data = xlrd.open_workbook(r'D:\yunshidata\Hospital_Data_Processing\1718.xls')
    table = data.sheets()[0]  
    nrows = table.nrows
    for row in range(1,nrows):
        print "OK"
        HCO_Name = table.cell(row,1).value
        result_list = connect_sqlserver(HCO_Name)
        if not result_list:
            continue
        result = ';'.join(result_list,row)
        save_data(result)
        print 'We Jave Proceessed The %d Data'% row
        print HCO_Name
        
# 将XMasterData数据导入到服务器数据库中
def Input_XMasterData():
    cursor = conn.cursor(as_dict=True) 
    cursor.execute("select * from dbo.Medical_org limit 10")
    for td in cursor:
        print str(td)
        
        
if __name__=='__main__':
    #get_data()
    #blur_match()
    Input_XMasterData()