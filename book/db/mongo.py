# coding=utf-8
# pymssql下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql

from pymongo import MongoClient


class MONGO:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def GetConnect(self):
        client = MongoClient(self.host, int(self.port))
        db = client.monitor
        # if self.user != '':
        #     db.authenticate(self.user,self.password)
        if not db:
            raise (NameError, '连接数据库失败')
        else:
            return db

    def save(self, collection,s):
        db = self.GetConnect()
        mycollection = db[collection]
        mycollection.insert_one(s)

    def ExecNonQuery(self, sql):
        cur = self.GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def GetData(self, sql):
        count = 0
        for i in range(len(sql)):
            for j in range(len(sql[i])):
                count += 1
                if type(sql[i][j]) is str:
                    print(sql[i][j].encode('latin1').decode('gbk'), end=',')
                else:
                    print(sql[i][j], end=',')
                if count % len(sql[i]) == 0:
                    print('\n')


if __name__ == '__main__':
    main()