# -*- coding: utf-8 -*-
from flask import Flask,request
from Hospital_Data_Processing import *
import MySQLdb
from flask import Blueprint
import json
import sys
import random
import time

reload(sys)
sys.setdefaultencoding('utf-8')


yunshi = Blueprint('yunshi', __name__)


"""
################################################医院数据校验###############################################
"""


# 连接mysql数据库
def Connect_Mysql():
    conn = MySQLdb.connect(charset="utf8", db="dev", host="182.92.96.114", user="remote", passwd="N4qXJn3Ms7P9Ksah")
    cur = conn.cursor()
    return cur, conn


# 获取所有医院信息
@yunshi.route('/getHospitalInfo', methods=['GET'])
def hospital_info():
    print "OK"
    try:
        dict_dir = Hospital_Info()
    except Exception, e:
        print e
    return json.dumps(dict_dir)


# 精确匹配医院信息,输入参数为{"id":"123456"}
@yunshi.route('/getAccurateMatch', methods=['POST'])
def accurate_match():
    param = {}
    param["id"] = request.form["id"]
    print param["id"]
    posts, cur = Connect_Mysql()
    sql1 = "SELECT status from dev.execlog WHERE id=%(id)s"
    sql2 = "UPDATE dev.execlog SET status= %(status)s WHERE id=%(id)s"
    data = posts.execute(sql1, param)
    result = posts.fetchmany(data)
    if not len(result):
        return json.dumps({"code": 0, "msg": "error"})
    if result[0][0] == 2:
        posts.execute("UPDATE dev.execlog SET typeid=1,status=3 WHERE id=%(id)s", param)
        cur.commit()
        try:
            get_accurate_match_info(param, posts, cur)
        except Exception, e:
            print e
            param["status"] = 0
            posts.execute(sql2, param)
            cur.commit()
            return json.dumps({"code": 0, "msg": "error"})
        param["status"] = 1
        posts.execute(sql2, param)
        cur.commit()
    return json.dumps({"code": 1, "msg": "success"})


# 模糊匹配医院信息
@yunshi.route('/getBlurMatch', methods=['POST'])
def blur_match():
    param = {}
    param["id"] = request.form["id"]
    posts, cur = Connect_Mysql()
    sql1 = "SELECT status from dev.execlog WHERE id=%(id)s"
    sql2 = "UPDATE dev.execlog SET status= %(status)s WHERE id=%(id)s"
    data = posts.execute(sql1, param)
    result = posts.fetchmany(data)
    if not len(result):
        return json.dumps({"code": 0, "msg": "error"})
    if result[0][0] == 2:
        posts.execute("UPDATE dev.execlog SET typeid=2,status=3 WHERE id=%(id)s", param)
        cur.commit()
        try:
            get_blur_match_info(param, posts, cur)
        except Exception, e:
            print e
            param["status"] = 0
            posts.execute(sql2, param)
            cur.commit()
            return json.dumps({"code": 0, "msg": "error"})
        param["status"] = 1
        posts.execute(sql2, param)
        cur.commit()
    return json.dumps({"code": 1, "msg": "success"})


# 根据提供的省、市、区信息查找相关医院信息,POST和GET请求都可以，POST请求格式{"Province":"辽宁省","City":"大连市","County":"沙河口区","Page":1,"Pagesize":15,"Param1":"医院","Param2":"","id":"abc001"}，GET请求格式Province=辽宁省&City=大连市&County=沙河口区
@yunshi.route('/getAllData', methods=['POST'])
def get_info():
    param = {}
    param["id"] = request.form["id"]
    param["Province"] = request.form['Province']
    param["City"] = request.form['City']
    param["County"] = request.form['County']
    param["Param1"] = request.form['Param1']
    param["Param2"] = request.form['Param2']
    param["page"] = request.form['Page']
    param["pagesize"] = request.form['Pagesize']
    if not param["page"]:
        param["page"] = 1
    if not param["pagesize"]:
        param["pagesize"] = 15
    if param["Province"] is None or param["City"] is None or param["County"] is None:
        return {"code": "2", "msg": "Params Error"}
    posts, cur = Connect_Mysql()
    sql1 = "SELECT status from dev.execlog WHERE id=%(id)s"
    sql2 = "UPDATE dev.execlog SET status= %(status)s WHERE id=%(id)s"
    data = posts.execute(sql1, param)
    result = posts.fetchmany(data)
    if not len(result):
        return json.dumps({"code": 0, "msg": "error"})
    if result[0][0] == 2:
        posts.execute("UPDATE dev.execlog SET typeid=3,status=3 WHERE id=%(id)s", param)
        cur.commit()
        try:
            dict_dir = get_all_thing(param, posts, cur)
        except Exception, e:
            print e
            param["status"] = 0
            posts.execute(sql2, param)
            cur.commit()
            return json.dumps({"code": 0, "msg": "error"})
        param["status"] = 1
        posts.execute(sql2, param)
        cur.commit()
    else:
        dict_dir = {"code": 1, "msg": "success", "content": []}
    return json.dumps(dict_dir)


# 根据医院ID查找相关医院信息
@yunshi.route('/getById', methods=['POST'])
def get_hospital_info():
    param = {}
    param["id"] = request.form["id"]
    posts, cur = Connect_Mysql()
    sql1 = "SELECT status from dev.execlog WHERE id=%(id)s"
    sql2 = "UPDATE dev.execlog SET status= %(status)s WHERE id=%(id)s"
    data = posts.execute(sql1, param)
    result = posts.fetchmany(data)
    if not len(result):
        return json.dumps({"code": 0, "msg": "error"})
    if result[0][0] == 2:
        posts.execute("UPDATE dev.execlog SET typeid=4,status=3 WHERE id=%(id)s", param)
        cur.commit()
        try:
            get_hospital_info_byId(param, posts, cur)
        except Exception, e:
            print e
            param["status"] = 0
            posts.execute(sql2, param)
            return json.dumps({"code": 0, "msg": "error"})
        param["status"] = 1
        posts.execute(sql2, param)
    return json.dumps({"code": 1, "msg": "success"})


# 导入医院信息
@yunshi.route('/InsertHospitalInfo', methods=['POST'])
def insert_hospital_info():
    param = {}
    param["id"] = request.form["id"]
    posts, cur = Connect_Mysql()
    sql1 = "SELECT status from dev.execlog WHERE id=%(id)s"
    sql2 = "UPDATE dev.execlog SET status= %(status)s WHERE id=%(id)s"
    data = posts.execute(sql1, param)
    result = posts.fetchmany(data)
    if not len(result):
        return json.dumps({"code": 0, "msg": "error"})
    if result[0][0] == 2:
        posts.execute("UPDATE dev.execlog SET typeid=5,status=3 WHERE id=%(id)s", param)
        cur.commit()
        try:
            Insert_Hospital_Info(param, posts, cur)
        except Exception, e:
            print e
            param["status"] = 0
            posts.execute(sql2, param)
            cur.commit()
            return json.dumps({"code": "0", "msg": "error"})
        param["status"] = 1
        posts.execute(sql2, param)
        cur.commit()
    return json.dumps({"code": "1", "msg": "success"})

