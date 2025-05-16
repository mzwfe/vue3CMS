# vue3CMS-backend/app/config.py
import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key_you_should_change' # JWT 和 Flask session 的密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    PORT = int(os.environ.get('FLASK_RUN_PORT', 5000))

    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'another_super_secret_jwt_key'
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DELTA_SECONDS = 3600 * 24 # Token 有效期，例如 24 小时

    # 数据库配置 (从环境变量获取)
    # 请在 .env 文件中设置这些值
    # 例如:
    # DB_HOST=localhost
    # DB_USER=your_db_user
    # DB_PASSWORD=your_db_password
    # DB_NAME=your_cms_database
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')  # 修改为用户提供的密码
    DB_NAME = os.environ.get('DB_NAME', 'cms_miaozhiwen') # 修改为用户提供的数据库名
    DB_PORT = os.environ.get('DB_PORT', '3306')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    # 生产环境可能需要更严格的配置
    # JWT_EXPIRATION_DELTA_SECONDS = 3600 # 例如，生产环境Token有效期更短

# 根据 FLASK_ENV 环境变量选择配置
config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    default=DevelopmentConfig
)

def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)