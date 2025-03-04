import pymongo
from datetime import datetime, timedelta
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
from models import User
import random
import time
from hashlib import sha256
import string

from config.setting import MONGODB_URL, MONGODB_DB_NAME


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
            db_url=MONGODB_URL,
            db_name=MONGODB_DB_NAME
            ):
        # MongoDB 连接
        try:
            self.client = pymongo.MongoClient(
                db_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
                )
            # 验证连接
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.users = self.db.users
            self.is_connected = True
        except Exception as e:
            self.is_connected = False
            raise Exception(f"连接数据库失败: {str(e)}")

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
                return True, user
            else:
                return False, "用户名或密码错误"
        except Exception as e:
            return False, f"登录失败: {str(e)}"
        
    def delete_account(
            self,
            default_id,
            password
            ):
        try:
            user = self.users.find_one({'_id': ObjectId(default_id)})
            if not user:
                return False, "用户不存在" 
            if user['password'] != hash_password(password):
                return False, "密码错误"
            result = self.users.update_one(
                {'_id': ObjectId(default_id)},
                {'$set': {'is_active': False,'deleted_at': datetime.utcnow()}}
            )
            return result.modified_count > 0, "账号已注销"
            
        except Exception as e:
            return False, f"注销失败: {str(e)}"
    
    def update_password(
            self,
            default_id,
            old_password,
            new_password
            ):
        try:
            user = self.users.find_one({'_id': ObjectId(default_id), 'is_active': True})
            if not user:
                return False, "用户不存在"
            if user['password'] != hash_password(old_password):
                return False, "原密码错误"
            result = self.users.update_one(
                {'_id': ObjectId(default_id)},
                {'$set': {'password': hash_password(new_password)}}
            )
            return result.modified_count > 0, "密码修改成功"
        except Exception as e:
            return False, f"密码修改失败: {str(e)}"
    
    def request_password_reset(
            self,
            email
            ):
        try:
            user = self.users.find_one({'email': email,'is_active': True})
            if not user:
                return False, "邮箱不存在或用户已注销"
            reset_code = generate_reset_code()
            expiry = datetime.utcnow() + timedelta(minutes=1)
            self.users.update_one(
                {'email': email},
                {'$set': {'reset_code': reset_code, 'reset_expiry': expiry}}
            )
            # TODO:发送邮件（这里先返回验证码，实际应该通过邮件发送）
            return True, reset_code
        except Exception as e:
            return False, {str(e)}
    
    def reset_password(
            self,
            email,
            reset_code,
            new_password
            ):
        try:
            user = self.users.find_one({
                'email': email, 
                'reset_code': reset_code,
                'reset_code_expiry': {'$gt': datetime.utcnow()}
                })
            if not user:
                return False, "验证码无效或已过期"
            # 更新密码并清除重置码
            result = self.users.update_one(
                {'email': email},
                {
                    '$set': {'password': hash_password(new_password)},
                    '$unset': {'reset_code': "", 'reset_code_expiry': ""}
                    }
            )
            return result.modified_count > 0, "密码重置成功"
        except Exception as e:
            return False, {str(e)}
        
    def get_user(self, user_id: str) -> Optional[User]:
        """获取单本书籍信息"""
        user_data = self.users.find_one({"_id": ObjectId(user_id)})
        return User(**user_data) if user_data else None