import pymysql
from twisted.enterprise import adbapi
from common.config import Config

class Mysql:
    def __init__(self) -> None:
        dbparams = dict(
            host = Config.get('mysql', 'host'), 
            port = int(Config.get('mysql', 'prot')),
            db = Config.get('mysql', 'dbname'),
            user= Config.get('mysql', 'user'),
            passwd = Config.get('mysql', 'passwd'),
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            use_unicode = False,   
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparams) 
        self.__dbpool = dbpool

    def connect(self):
        return self.__dbpool

    def __del__(self):
        try:
            self.__dbpool.close()
        except Exception as ex:
            print(ex)

Mysql = Mysql()