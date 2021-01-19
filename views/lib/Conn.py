# -*- coding: UTF-8 -*-
from pymongo import MongoClient


# 数据库连接
class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database='xunfeng', username='', password=''):
        self.host = host
        self.port = port
        self.database = database
        self.conn = MongoClient(f'mongodb://{username}:{password}@{self.host}:{self.port}/{self.database}')
        self.coll = self.conn[self.database]
        self.coll.authenticate(username, password)
