# -*- coding: utf-8 -*-
from pymongo import MongoClient


def get_db(db=None):
    if db is not None:
        cursor = MongoClient(host="182.92.96.114", port=27017)
        conn = cursor[db]
        conn.authenticate("root", "123456")
    else:
        cursor = MongoClient(host="182.92.96.114", port=27017)
        conn = cursor.YunshiDB_Hospital_Info
        conn.authenticate("root", "123456")
    return conn