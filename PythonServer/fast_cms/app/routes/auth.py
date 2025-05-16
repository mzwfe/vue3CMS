# vue3CMS-backend/app/routes/auth.py
from flask import Blueprint, request, jsonify, current_app
from app.utils.auth_utils import generate_token, verify_password, token_required, hash_password
import pymysql
import traceback
from app.config import get_config

bp = Blueprint('auth', __name__)

def get_db_connection():
    """使用pymysql方式获取数据库连接，与test_pymysql.py保持一致"""
    config = get_config()
    try:
        conn = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=int(config.DB_PORT),
            database=config.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        current_app.logger.error(f"数据库连接错误: {e}")
        traceback.print_exc()
        return None

@bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('password'):
        return jsonify({"code": 400, "message": "用户名和密码不能为空"}), 400

    username = data.get('name')
    password = data.get('password')

    try:
        # 使用pymysql方式连接数据库
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
        
        cursor = conn.cursor()

        # 查询用户信息
        query = "SELECT id, name, password, role_id FROM users WHERE name = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        # 添加安全的密码验证
        authenticated = False
        if user:
            try:
                authenticated = verify_password(user['password'], password)
            except Exception as e:
                current_app.logger.error(f"密码验证出错: {e}")
                # 密码格式不正确，验证失败但不抛出异常
                authenticated = False

        if user and authenticated:
            # 查询角色信息
            role_info = {"id": None, "name": ""}
            if user['role_id']:
                role_query = "SELECT id, name, intro FROM roles WHERE id = %s"
                cursor.execute(role_query, (user['role_id'],))
                role = cursor.fetchone()
                if role:
                    role_info = {"id": role['id'], "name": role['name']}

            cursor.close()
            conn.close()

            # 生成token
            token_str = generate_token(user['id'], user['name'], role_info)

            if token_str:
                return jsonify({
                    "code": 0,
                    "data": {
                        "id": user['id'],
                        "name": user['name'],
                        "token": token_str
                    }
                }), 200
            else:
                return jsonify({"code": 500, "message": "生成Token失败"}), 500
        else:
            cursor.close()
            conn.close()
            return jsonify({"code": 401, "message": "用户名或密码错误"}), 401

    except Exception as e:
        current_app.logger.error(f"Login error: {e}")
        if 'cursor' in locals() and cursor: cursor.close()
        if 'conn' in locals() and conn: conn.close()
        return jsonify({"code": 500, "message": f"登录时发生服务器错误: {str(e)}"}), 500

@bp.route('/register', methods=['POST'])
def register():
    """注册新用户接口"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('password'):
        return jsonify({"code": 400, "message": "用户名和密码不能为空"}), 400

    username = data.get('name')
    password = data.get('password')
    realname = data.get('realname', username)
    cellphone = data.get('cellphone', '')
    role_id = data.get('role_id', 2)  # 默认为普通用户角色
    department_id = data.get('department_id', 1)  # 默认部门ID

    conn = None
    cursor = None
    try:
        # 使用pymysql方式连接数据库
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
        
        cursor = conn.cursor()
        
        # 检查用户是否已存在
        cursor.execute("SELECT id FROM users WHERE name = %s", (username,))
        if cursor.fetchone():
            return jsonify({"code": 409, "message": "用户名已存在"}), 409
        
        # 对密码进行加密
        hashed_password = hash_password(password)
        
        # 插入新用户
        insert_query = """
        INSERT INTO users (name, password, realname, cellphone, role_id, department_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (username, hashed_password, realname, cellphone, role_id, department_id))
        conn.commit()
        
        # 获取新创建的用户ID
        user_id = cursor.lastrowid
        
        return jsonify({
            "code": 0, 
            "message": "用户注册成功",
            "data": {"id": user_id}
        }), 201
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Registration error: {e}")
        return jsonify({"code": 500, "message": f"注册失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/test', methods=['GET'])
@token_required
def test_token(current_user_payload):
    """验证Token是否有效的测试接口"""
    return jsonify({
        "code": 0,
        "message": "Token验证成功!",
        "data": current_user_payload
    }), 200

@bp.route('/user_info', methods=['GET'])
@token_required
def get_user_info(current_user_payload):
    """获取当前登录用户的详细信息"""
    user_id = current_user_payload.get('id')
    
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
        
        cursor = conn.cursor()
        
        # 查询用户详细信息
        query = """
        SELECT u.id, u.name, u.realname, u.cellphone, u.role_id, u.department_id, 
               r.name as role_name, r.intro as role_intro, 
               d.name as department_name, d.leader as department_leader
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        LEFT JOIN departments d ON u.department_id = d.id
        WHERE u.id = %s
        """
        cursor.execute(query, (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            return jsonify({"code": 404, "message": "用户不存在"}), 404
        
        # 格式化用户信息
        result = {
            "id": user_data["id"],
            "name": user_data["name"],
            "realname": user_data["realname"],
            "cellphone": user_data["cellphone"],
            "role": {
                "id": user_data["role_id"],
                "name": user_data["role_name"],
                "intro": user_data["role_intro"]
            },
            "department": {
                "id": user_data["department_id"],
                "name": user_data["department_name"],
                "leader": user_data["department_leader"]
            }
        }
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "code": 0,
            "data": result
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user info error: {e}")
        if 'cursor' in locals() and cursor: cursor.close()
        if 'conn' in locals() and conn: conn.close()
        return jsonify({"code": 500, "message": f"获取用户信息时发生错误: {str(e)}"}), 500