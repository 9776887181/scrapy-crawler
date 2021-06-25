import redis
from common.config import Config

class Redis:
    def __init__(self):
        dbparams = dict(
            host = Config.get('redis', 'host'), 
            port = Config.get('redis', 'port'), 
            db = Config.get('redis', 'db'),
            decode_responses = True,
        )
        self.__pool = redis.ConnectionPool(**dbparams)
        self.__connect = redis.Redis(connection_pool = self.__pool)

    def connect(self):
        return self.__connect

    def __del__(self):
        self.__connect.close()

Redis = Redis()

