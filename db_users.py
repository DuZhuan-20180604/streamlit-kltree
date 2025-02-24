import pymongo
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from models import User
import random
import time
from hashlib import sha256
import string

def generate_user_id():
    timestamp = int(time.time() * 1000)
    random_num = random.randint(0, 999)
    return f"U{timestamp % 10000}{random_num:03d}" 

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def generate_reset_code():
    """生成6位验证码"""
    return ''.join(random.choices(string.digits, k=6))

class UserManager:
    def __init__(
            self,
            db_url="mongodb://localhost:27017/",
            ):
        # MongoDB 连接
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client['math_learning_db']
        self.users = self.db.users

    def register(
        self,
        username, 
        email, 
        password, 
        ):
        try:
            if self.users.find_one({'$or': [{'username': username}, {'email': email}]}):
                return False, "用户名或邮箱已存在"
            
            user_id= generate_user_id()
            hashed_password = hash_password(password)

            user = User(
                user_id=user_id,
                username=username,
                email=email,
                password=hashed_password,
                role="USER",
                created_at=datetime.utcnow(),
                last_login=None,
                is_active=True
            )
            self.users.insert_one(user.dict())
            return True, "注册成功，请到登录页登录"
        except Exception as e:
            return False, f"注册失败: {str(e)}"
    
    def login(
            self,
            identifier, 
            password
            ):
        try:
            user = self.users.find_one({
                '$or': [
                    {'username': identifier},
                    {'email': identifier},
                    {'user_id': identifier}
                ],
                'password': hash_password(password),
                'is_active': True
            })
            if user:
                self.users.update_one(
                    {'_id':user['_id']},
                    {'$set': {'last_login': datetime.utcnow()}}
                )
                return True, "登录成功"
            else:
                return False, "用户名或密码错误"
        except Exception as e:
            return False, f"登录失败: {str(e)}"
    