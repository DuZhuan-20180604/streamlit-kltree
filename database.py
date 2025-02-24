import pymongo
from datetime import datetime

class Database:
    def __init__(self):
        # MongoDB 连接
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['math_learning_db']
        self.users = self.db.users
        
        # 删除旧的索引
        self.users.drop_indexes()
        # 创建索引
        self._create_indexes()
    
    def _create_indexes(self):
        # 用户集合的唯一索引
        self.users.create_index([("username", 1)], unique=True)
        self.users.create_index([("email", 1)], unique=True)
        self.users.create_index([("user_id", 1)], unique=True)

    def close(self):
        self.client.close()

# 创建全局数据库实例
db = Database()