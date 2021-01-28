# coding=utf-8
# pymssql下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql

import redis


class REDIS:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def GetConnect(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, decode_responses=True)
        r = redis.Redis(connection_pool=self.pool)
        if not r:
            raise (NameError, '连接数据库失败')
        else:
            return r

    def setKey(self,key,value):
        r = self.GetConnect()
        r.set(key,str(value))
        pass

    def getValue(self,key):
        r = self.GetConnect()
        value = r.get(key)
        return value
        pass