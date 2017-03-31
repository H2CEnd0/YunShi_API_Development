# -*- coding: utf-8 -*-
import MySQLdb


class MySQL_db(object):
    def __init__(self):
        self.db = MySQLdb.connect("182.92.96.114", "remote", "N4qXJn3Ms7P9Ksah", "PD_Voice_APP3.0")
        self.cursor = self.db.cursor()

    def insert_info(self, info):
        sql = """INSERT INTO PD_Voice_Record(User_ID, Type, age, sex, time_stamp, label, UPRDS, Fo, Fhi, Flo,
Fosd, `Jitter(%%)`, `Jitter(Abs)`, `Jitter(RAP)`, `Jitter(PPQ5)`, `Jitter(DDP)`, Shimmer, `Shimmer(dB)`, `Shimmer(APQ3)`,
`Shimmer(APQ5)`, `Shimmer(APQ11)`, `Shimmer(DDA)`)VALUES (%(userid)s, %(Type)s, %(age)s, %(sex)s, %(time_stamp)s,
%(label)s, %(uprds)s, %(fo)s, %(fhi)s, %(flo)s, %(fosd)s, %(jitter(%))s, %(jitter(Abs))s, %(jitter(RAP))s,
%(jitter(PPQ5))s, %(jitter(DDP))s, %(shimmer)s, %(shimmer(dB))s, %(shimmer(APQ3))s, %(shimmer(APQ5))s,
%(shimmer(APQ11))s, %(shimmer(DDA))s)"""
        self.cursor.execute(sql, info)
        self.db.commit()

    def find_by_id(self,id):
        sql = "select * from PD_Voice_Record where id='%d'" % id
        result = self.cursor.execute(sql)
        info = self.cursor.fetchmany(result)
        return info