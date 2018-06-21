# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 21:23
# @Author  : 
# @File    : sqlite_action.py
# @Software: PyCharm Community Edition

import sqlite3
class Do_Sql():
    def __init__(self, db_file_name):
        # sql_file='demo.db'
        self.cx = sqlite3.connect(db_file_name)
        self.cu=self.cx.cursor()

    def exe_sql(self, sql):
        # sql='create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE)'
        self.cu.execute(sql)
        self.cx.commit()
    def select_sql(self,sql):
        self.cu.execute(sql)
        return self.cu.fetchall()