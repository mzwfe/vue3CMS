# vue3CMS-backend/app/utils/auth_utils.py
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

# --- 密码处理 ---
def hash_password(password):
    """生成密码的哈希值"""
    return generate_password_hash(password)

def verify_password(hashed_password, password_to_check):
    """验证密码"""
    return check_password_hash(hashed_password, password_to_check)

# --- JWT Token 处理 ---
def generate_token(user_id, user_name, role_info):
    """
    生成认证 Token
    :param user_id: 用户id
    :param user_name: 用户名
    :param role_info: 角色信息 (可以是一个字典，例如包含角色ID和角色名)
    :return: token
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=current_app.config['JWT_EXPIRATION_DELTA_SECONDS']),
            'iat': datetime.datetime.utcnow(),
            'id': user_id, # 根据接口文档，token payload 包含 id, name, role
            'name': user_name,
            'role': role_info # 例如: {"id": 1, "name": "超级管理员"}
        }
        return jwt.encode(
            payload,
            current_app.config['JWT_SECRET_KEY'],
            algorithm=current_app.config['JWT_ALGORITHM']
        )
    except Exception as e:
        current_app.logger.error(f"Error generating token: {e}")
        return None

def decode_token(token):
    """
    解码 Token
    :param token: token字符串
    :return: payload字典或None
    """
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
        return payload
    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Token expired.")
        return "Token expired"
    except jwt.InvalidTokenError:
        current_app.logger.warning("Invalid token.")
        return "Invalid token"
    except Exception as e:
        current_app.logger.error(f"Error decoding token: {e}")
        return None

# --- 装饰器：用于需要认证的接口 ---
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"code": 401, "message": "Token is missing!"}), 401

        try:
            data = decode_token(token)
            if isinstance(data, str): # 如果解码返回的是错误信息字符串
                return jsonify({"code": 401, "message": data}), 401
            if data is None or 'id' not in data:
                return jsonify({"code": 401, "message": "Token is invalid or payload incomplete!"}), 401

            # 可以将解码后的用户信息（例如用户ID）传递给路由函数
            # current_user_id = data['id']
            # g.current_user_id = data['id'] # 使用 g 对象在请求上下文中传递
        except Exception as e:
            current_app.logger.error(f"Token validation error: {e}")
            return jsonify({"code": 401, "message": "Token is invalid!"}), 401

        # 将解码后的 payload 或特定用户信息传递给视图函数
        return f(data, *args, **kwargs) # data 是解码后的 payload

    return decorated_function