import pymongo


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class Conn:
    def __init__(self):
        self._conn = pymongo.MongoClient("127.0.0.1", 27017)
        self._db = self._conn["ACDB"]

    def insert(self, col, doc):
        if type(doc) == list:
            return self._db[col].insert_many(doc)
        else:
            return self._db[col].insert_one(doc)

    def find(self, col, condition):
        return self._db[col].find(condition)

    def update(self, col, condition, term):
        return self._db[col].update_many(condition, term)

    def delete(self, col, condition):
        return self._db[col].delete_many(condition)


conn = Conn()
