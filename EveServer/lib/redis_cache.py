# -*- encoding:utf-8 -*-

from config import Config
import redis
import json

class Cache(object):

    __cache = None

    def __new__(cls, *args, **kwargs):
        if not cls.__cache:
            cls.__cache = super(Cache, cls).__new__(cls, *args, **kwargs)
        return cls.__cache

    def __init__(self, host, port, db):
        self.redis = redis.Redis(host=host, port=port, db=db)

    @property
    def keys(self):
        return self.redis.keys()

    def cache(self, key, value, timeout=3600*12):
        self.redis.set(key, json.dumps(value))
        self.redis.expire(key, timeout)

    def hasKey(self, key):
        return key in self.keys

    def getKey(self, key):
        return self.redis.get(key)