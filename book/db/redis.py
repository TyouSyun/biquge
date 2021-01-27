# coding=utf-8
# pymssql下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql

import redis


class REDIS:
    def __init__(self, host, port, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def GetConnect(self):
        self.pool = pymssql.ConnectionPool(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        red = redis.Redis(connection_pool=self.pool)
        if not red:
            raise (NameError, '连接数据库失败')
        else:
            return red