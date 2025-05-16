# app/utils/auth_utils.py
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def hash_password(password):
    """
    对密码进行哈希处理
    """
    # 生成salt并对密码进行哈希
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # 存储为字符串

def verify_password(hashed_password, password):
    """
    验证密码是否匹配
    """
    try:
        # 检查是否为有效的bcrypt哈希
        if not hashed_password or not isinstance(hashed_password, str) or not password:
            return False
            
        # 检查是否是bcrypt格式的哈希值
        if not (hashed_password.startswith('$2a$') or hashed_password.startswith('$2b$')):
            current_app.logger.warning(f"密码格式不正确，不是有效的bcrypt哈希: {hashed_password[:6]}...")
            return False
            
        # 将哈希密码和提供的密码进行比较
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        current_app.logger.error(f"密码验证过程出错: {e}")
        return False

def generate_token(user_id, username, role_info):
    """
    生成JWT令牌
    """
    try:
        # 设置令牌的有效期（例如24小时）
        expiration = datetime.utcnow() + timedelta(hours=24)
        
        # 创建令牌的payload
        payload = {
            'id': user_id,
            'name': username,
            'role': role_info,
            'exp': expiration
        }
        
        # 使用密钥签名并生成令牌
        token = jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY', 'fallback_secret_key'),
            algorithm='HS256'
        )
        
        # 在Python 3.6+中，jwt.encode返回字节，需要解码为字符串
        if isinstance(token, bytes):
            return token.decode('utf-8')
        return token
    
    except Exception as e:
        current_app.logger.error(f"Token generation error: {e}")
        return None

def token_required(f):
    """
    验证JWT令牌的装饰器
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取令牌
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'code': 401, 'message': '缺少认证令牌'}), 401
        
        try:
            # 解码令牌并验证
            payload = jwt.decode(
                token, 
                current_app.config.get('SECRET_KEY', 'fallback_secret_key'),
                algorithms=['HS256']
            )
            
            # 将解码后的用户信息传递给被装饰的函数
            return f(payload, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'code': 401, 'message': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'code': 401, 'message': '无效的令牌'}), 401
        
    return decorated 