from datetime import datetime,timedelta
from hashlib import sha256
from database import db
import time
import random
import string

class Auth:
    
    @staticmethod
    def generate_user_id():
        timestamp = int(time.time() * 1000)
        random_num = random.randint(0, 999)
        return f"U{timestamp % 10000}{random_num:03d}"

    @staticmethod
    def hash_password(password):
        return sha256(password.encode()).hexdigest()
    
    @staticmethod
    def generate_reset_code():
        """生成6位验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    @staticmethod
    def register(username, email, password, role='USER'):
        try:
            if db.users.find_one({'$or': [{'username': username}, {'email': email}]}):
                return False, "用户名或邮箱已存在"
            #user_id = Auth.generate_user_id()
            #while db.users.find_one({'user_id': user_id}):
            #    user_id = Auth.generate_user_id()
            
            user = {
                'user_id': Auth.generate_user_id(),
                'username': username,
                'email': email,
                'password': Auth.hash_password(password),
                'role': role,
                'created_at': datetime.utcnow(),
                'last_login': None,
                'is_active': True
            }
            db.users.insert_one(user)
            return True, "注册成功，请到登录页登录"
        except Exception as e:
            return False, f"注册失败: {str(e)}"

    @staticmethod
    def login(identifier, password):
        try:
            user = db.users.find_one({
                '$or': [
                    {'username': identifier},
                    {'email': identifier},
                    {'user_id': identifier}
                ],
                'password': Auth.hash_password(password),
                'is_active': True
            })
            if user:
                db.users.update_one(
                    {'_id': user['_id']},
                    {'$set': {'last_login': datetime.utcnow()}}
                )
            return user is not None, user
        except Exception as e:
            return False, None
        
    @staticmethod
    def delete_account(user_id,password):
        try:
            user = db.users.find_one({'_id': user_id})
            if not user:
                return False, "用户不存在" 
            
            
            if user['password'] != Auth.hash_password(password):
                return False, "密码错误"
            
            # 软删除：标记为非活动
            result = db.users.update_one(
                {'_id': user_id},
                {'$set': {'is_active': False, 'deleted_at': datetime.utcnow()}}
            )
            return result.modified_count > 0, "账号已注销"
        except Exception as e:
            return False, f"注销失败: {str(e)}"
        
    @staticmethod
    def update_password(user_id, old_password, new_password):
        try:
            user = db.users.find_one({'_id': user_id, 'is_active': True})
            if not user or user['password'] != Auth.hash_password(old_password):
                return False, "原密码错误"
            
            result = db.users.update_one(
                {'_id': user_id},
                {'$set': {'password': Auth.hash_password(new_password)}}
            )
            return result.modified_count > 0, "密码已更新"
        except Exception as e:
            return False, f"密码更新失败: {str(e)}"
        
    @staticmethod
    def request_password_reset(email):
        """请求密码重置"""
        try:
            user = db.users.find_one({'email': email, 'is_active': True})
            if not user:
                return False, "邮箱不存在或用户已注销"
            
            # 生成重置码并存储
            reset_code = Auth.generate_reset_code()
            expiry = datetime.utcnow() + timedelta(minutes=1)
            
            db.users.update_one(
                {'email': email},
                {
                    '$set': {
                        'reset_code': reset_code,
                        'reset_code_expiry': expiry
                    }
                }
            )
            
            # TODO: 发送邮件（这里先返回验证码，实际应该通过邮件发送）
            return True, reset_code
        except Exception as e:
            return False, str(e)
        
    @staticmethod
    def reset_password(email, reset_code, new_password):
        """重置密码"""
        try:
            user = db.users.find_one({
                'email': email,
                'reset_code': reset_code,
                'reset_code_expiry': {'$gt': datetime.utcnow()}
            })
            
            if not user:
                return False, "验证码无效或已过期"
            
            # 更新密码并清除重置码
            db.users.update_one(
                {'email': email},
                {
                    '$set': {'password': Auth.hash_password(new_password)},
                    '$unset': {'reset_code': "", 'reset_code_expiry': ""}
                }
            )
            return True, "密码重置成功"
        except Exception as e:
            return False, str(e)