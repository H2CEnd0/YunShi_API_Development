# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask import Blueprint
from MySQL_db import MySQL_db
import matlab
import matlab.engine
import sys
import random
import time

reload(sys)
sys.setdefaultencoding("utf-8")

bupa = Blueprint("bupa", __name__)


# 根据UserId输出用户帕金森病测试历史纪录,输入参数格式为{"UserId":"12474"}
@bupa.route('/Query', methods=['POST'])
def get_tasks():
    database = MySQL_db()
    UserId = request.form["UserId"]
    info = database.find_by_id(int(UserId))
    result = []
    for res in info:
        dict = {}
        dict["id"] = res[0]
        dict["timestamp"] = res[1]
        dict["UPRDS"] = res[3]
        result.append(dict)
    return jsonify({"result": result, "msg": "success"})


# 根据语音，解析语音，通过机器学习算法计算得帕金森病的可能性值，返回给前端显示
@bupa.route("/Test_Voice", methods=["POST"])
def PD_Test():
    cursor = MySQL_db()
    time1 = time.time()
    File_number = int(request.form["file_number"])
    filename = request.form["file_name"]
    Path_data = "/mnt/newdata/PD_Voice/voice/" + filename + "_"
    eng = matlab.engine.connect_matlab()
    feature_values = eng.voice_deal(Path_data, File_number)
    eng.quit()
    if len(list(feature_values)) == 1:
        return jsonify({"value": int(feature_values[0])})
    feature_param = ["label", "uprds", "fo", "fhi", "flo", "fosd", "jitter(%)", "jitter(Abs)", "jitter(RAP)",
                     "jitter(PPQ5)", "jitter(DDP)", "shimmer", "shimmer(dB)", "shimmer(APQ3)", "shimmer(APQ5)",
                     "shimmer(APQ11)", "shimmer(DDA)"]
    sql_param = dict(zip(feature_param, feature_values))
    sql_param["userid"] = filename.split("_")[0]
    sql_param["Type"] = request.form["type"]
    sql_param["age"] = request.form["age"]
    sql_param["sex"] = request.form["sex"]
    sql_param["time_stamp"] = filename.split("_")[1]
    cursor.insert_info(sql_param)
    time2 = time.time()
    print time2-time1
    return jsonify({"value": int(feature_values[1])})

