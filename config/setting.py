import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
#MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
#MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'math_learning_db')
MONGODB_URL=os.environ.get('MONGODB_URL')
MONGODB_DB_NAME=os.environ.get('MONGODB_DB_NAME')






