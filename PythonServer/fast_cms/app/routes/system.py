# vue3CMS-backend/app/routes/system.py
from flask import Blueprint, request, jsonify, current_app
import pymysql
import traceback
from app.utils.auth_utils import token_required, hash_password
from datetime import datetime, timedelta
from app.config import get_config

bp = Blueprint('system', __name__)

def get_db_connection():
    """使用pymysql方式获取数据库连接，与auth.py保持一致"""
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

# --- Helper function to convert Row to Dict ---
def row_to_dict(row):
    if row is None:
        return None
    # 对于 datetime 对象，转换为 ISO 格式字符串
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, datetime):
            d[key] = value.isoformat() + 'Z' # 模仿接口文档中的格式
    return d

def rows_to_list_of_dicts(rows):
    return [row_to_dict(row) for row in rows]

# --- 用户管理 ---
@bp.route('/users', methods=['POST'])
@token_required
def create_user(current_user_payload):
    """创建用户"""
    data = request.get_json()
    required_fields = ['name', 'realname', 'password', 'cellphone', 'departmentId', 'roleId']
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "缺少必要参数"}), 400

    hashed_pwd = hash_password(str(data['password'])) # 密码确保是字符串

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # 检查用户名是否已存在
        cursor.execute("SELECT id FROM users WHERE name = %s", (data['name'],))
        if cursor.fetchone():
            return jsonify({"code": 409, "message": "用户名已存在"}), 409

        sql = """
            INSERT INTO users (name, realname, password, cellphone, department_id, role_id, createAt, updateAt)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(sql, (
            data['name'], data['realname'], hashed_pwd, str(data['cellphone']),
            data['departmentId'], data['roleId']
        ))
        conn.commit()
        # Postman 文档中创建用户成功后返回的响应体比较简单，这里遵循一下
        # 如果需要返回创建的用户信息，可以查询后返回
        return jsonify({"code": 0, "data": {"message": "创建用户成功", "id": cursor.lastrowid}}), 201
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create user error: {e}")
        return jsonify({"code": 500, "message": f"创建用户失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user_payload, user_id):
    """删除用户"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"code": 0, "data": "删除用户成功"}), 200
        else:
            return jsonify({"code": 404, "message": "用户不存在"}), 404
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Delete user error: {e}")
        return jsonify({"code": 500, "message": f"删除用户失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/users/<int:user_id>', methods=['PATCH'])
@token_required
def update_user(current_user_payload, user_id):
    """修改用户"""
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求体不能为空"}), 400

    update_fields = []
    params = []

    if 'password' in data:
        update_fields.append("password = %s")
        params.append(hash_password(str(data['password'])))
    if 'cellphone' in data:
        update_fields.append("cellphone = %s")
        params.append(str(data['cellphone']))
    # 可以根据需要添加其他可修改字段: realname, enable, role_id, department_id

    if not update_fields:
        return jsonify({"code": 400, "message": "没有提供可更新的字段"}), 400

    update_fields.append("updateAt = NOW()")
    params.append(user_id)

    sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"code": 0, "data": "修改用户成功"}), 200
        else:
            return jsonify({"code": 404, "message": "用户不存在或数据未更改"}), 404
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Update user error: {e}")
        return jsonify({"code": 500, "message": f"修改用户失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user_payload, user_id):
    """查询某个用户"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 根据Postman响应体，需要联查role和department信息
        sql = """
            SELECT 
                u.id, u.name, u.realname, u.cellphone, u.enable, 
                u.createAt, u.updateAt,
                r.id as role_id, r.name as role_name, r.intro as role_intro, 
                r.createAt as role_createAt, r.updateAt as role_updateAt,
                d.id as department_id, d.name as department_name, d.parentId as department_parentId, 
                d.leader as department_leader, d.createAt as department_createAt, d.updateAt as department_updateAt
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id
            LEFT JOIN departments d ON u.department_id = d.id
            WHERE u.id = %s
        """
        cursor.execute(sql, (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            # 格式化成接口文档的响应结构
            response_data = {
                "id": user_data["id"],
                "name": user_data["name"],
                "realname": user_data["realname"],
                "cellphone": int(user_data["cellphone"]) if user_data["cellphone"] else None, # API返回数字
                "enable": user_data["enable"],
                "createAt": user_data["createAt"].isoformat() + "Z" if user_data["createAt"] else None,
                "updateAt": user_data["updateAt"].isoformat() + "Z" if user_data["updateAt"] else None,
                "role": None,
                "department": None
            }
            if user_data["role_id"]:
                response_data["role"] = {
                    "id": user_data["role_id"],
                    "name": user_data["role_name"],
                    "intro": user_data["role_intro"],
                    "createAt": user_data["role_createAt"].isoformat() + "Z" if user_data["role_createAt"] else None,
                    "updateAt": user_data["role_updateAt"].isoformat() + "Z" if user_data["role_updateAt"] else None
                }
            if user_data["department_id"]:
                response_data["department"] = {
                    "id": user_data["department_id"],
                    "name": user_data["department_name"],
                    "parentId": user_data["department_parentId"],
                    "leader": user_data["department_leader"],
                    "createAt": user_data["department_createAt"].isoformat() + "Z" if user_data["department_createAt"] else None,
                    "updateAt": user_data["department_updateAt"].isoformat() + "Z" if user_data["department_updateAt"] else None
                }
            return jsonify({"code": 0, "data": response_data}), 200
        else:
            return jsonify({"code": 404, "message": "用户不存在"}), 404
    except Exception as e:
        current_app.logger.error(f"Get user error: {e}")
        return jsonify({"code": 500, "message": f"查询用户失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@bp.route('/users/list', methods=['POST']) # Postman 文档中使用POST
@token_required
def get_user_list(current_user_payload):
    """查询用户列表"""
    data = request.get_json()
    offset = data.get('offset', 0) # 默认为0，但Postman中是1，需注意分页逻辑
    size = data.get('size', 10)
    realname_filter = data.get('realname') # 可选的真实姓名筛选

    # 调整 offset 以适应 SQL LIMIT (通常从0开始)
    # 如果接口定义的 offset 从 1 开始，则 page_offset = offset - 1 (如果offset > 0 else 0)
    # 这里假设接口的 offset 已经是数据库期望的 (例如 0-indexed)
    # 或者如果前端传1代表第一页，则 (page-1)*size

    # 接口文档中offset: 1, size: 10
    # SQL LIMIT 通常是 LIMIT offset, count (LIMIT (page-1)*size, size)
    # 若接口的offset是记录的起始位置（如SQL），则可直接用
    # 若接口的offset是页码，则需要转换
    # 假设接口的 offset 是记录的起始偏移量，但Postman示例为1，可能指跳过1条，取第2条开始？
    # 或者 offset 指页码。多数情况 offset=0, limit=10 是第一页。
    # Postman中，offset: 1, size: 10, realname: "c"
    # 响应中 totalCount: 2, list 只有一个用户。如果 offset: 1 指的是跳过1条，那么结果应该不同。
    # 通常 offset 指的是跳过的记录数。
    # 如果前端传的是页码，如 page:1, size:10 -> offset=(page-1)*size
    # 鉴于Postman的 `offset: 1, size: 10`，我们假设它指的是从第 `offset` 条记录开始（1-indexed），或者跳过 `offset` 条。
    # 为了安全和常见做法，我们将其视为 0-indexed offset。如果Postman确实是1-indexed的记录开始，则需要调整。
    # 接口文档查询用户列表的响应体中，offset: 1, size: 10 返回了 id: 1 的用户， totalCount: 2。
    # 这表明 offset: 1 可能意味着 "从第1条开始" 或者 "跳过0条"。
    # 如果 offset 是页码，page 1 -> offset 0.
    # 我们按照 Postman 示例，如果 offset=1, 数据库中应该是 LIMIT 0, size (如果offset是页码)
    # 或者 LIMIT offset, size (如果 offset 是记录跳过数，且从0开始)。
    # 响应中 totalCount: 2, list 只有一条数据.
    # 如果 `offset: 1, size: 10, realname: "c"`，响应是`id: 1, totalCount: 2`
    # 让我们假设 Postman 的 offset 是 1-indexed 页码，而 size 是每页数量。
    # page = data.get('offset', 1)
    # limit = data.get('size', 10)
    # sql_offset = (page - 1) * limit
    # 上述假设不符合Postman给的 "offset: 1, size: 10" 得到id:1的结果。
    # 更可能是 offset 是起始位置（0-indexed）。但Postman用1，这是一个常见混淆点。
    # 严格按照Postman给的参数"offset": 1, "size": 10，如果返回的是第一条，那这个offset就不是标准的SQL offset。
    # 我们这里将接口的 offset 理解为 SQL 的 offset（跳过的行数）
    sql_offset = int(offset) if offset else 0
    sql_limit = int(size) if size else 10


    params = []
    where_clauses = []

    if realname_filter:
        where_clauses.append("realname LIKE %s")
        params.append(f"%{realname_filter}%")

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        count_sql = f"SELECT COUNT(*) as totalCount FROM users {where_sql}"
        cursor.execute(count_sql, tuple(params))
        total_count = cursor.fetchone()['totalCount']

        # 根据Postman响应体，用户列表不包含role和department的详细对象，而是roleId和departmentId
        list_sql = f"""
            SELECT id, name, realname, cellphone, enable, department_id as departmentId, role_id as roleId, createAt, updateAt 
            FROM users 
            {where_sql}
            ORDER BY id ASC 
            LIMIT %s, %s
        """

        # params_for_list = params + [sql_offset, sql_limit] # This is wrong if params can be empty
        final_params_for_list = list(params) # Create a mutable copy
        final_params_for_list.append(sql_offset)
        final_params_for_list.append(sql_limit)

        cursor.execute(list_sql, tuple(final_params_for_list))
        users_list = cursor.fetchall()

        formatted_users_list = []
        for user in users_list:
            formatted_user = {
                "id": user["id"],
                "name": user["name"],
                "realname": user["realname"],
                "cellphone": int(user["cellphone"]) if user["cellphone"] else None, # API返回数字
                "enable": user["enable"],
                "departmentId": user["departmentId"],
                "roleId": user["roleId"],
                "createAt": user["createAt"].isoformat() + "Z" if user["createAt"] else None,
                "updateAt": user["updateAt"].isoformat() + "Z" if user["updateAt"] else None
            }
            formatted_users_list.append(formatted_user)

        return jsonify({
            "code": 0,
            "data": {
                "list": formatted_users_list,
                "totalCount": total_count
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get user list error: {e}")
        return jsonify({"code": 500, "message": f"查询用户列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- 部门管理 ---
@bp.route('/department', methods=['POST'])
@token_required
def create_department(current_user_payload):
    data = request.get_json()
    if not data or not data.get('name') or not data.get('leader'): # parentId is optional
        return jsonify({"code": 400, "message": "部门名称和负责人不能为空"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO departments (name, parentId, leader, createAt, updateAt) VALUES (%s, %s, %s, NOW(), NOW())"
        cursor.execute(sql, (data['name'], data.get('parentId'), data['leader']))
        conn.commit()
        # 接口文档响应 "创建部门成功~"
        return jsonify({"code": 0, "data": "创建部门成功~"}), 201 # 或者返回创建的部门信息
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create department error: {e}")
        return jsonify({"code": 500, "message": f"创建部门失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/department/<int:dept_id>', methods=['DELETE'])
@token_required
def delete_department(current_user_payload, dept_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 注意：如果存在子部门，直接删除可能会失败或违反逻辑（取决于数据库如何处理无物理外键的情况下的级联）
        # 应用层面可能需要先检查是否有子部门或用户关联
        cursor.execute("DELETE FROM departments WHERE id = %s", (dept_id,))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"code": 0, "data": "删除部门成功"}), 200
        else:
            return jsonify({"code": 404, "message": "部门不存在"}), 404
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Delete department error: {e}")
        return jsonify({"code": 500, "message": f"删除部门失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/department/<int:dept_id>', methods=['PATCH'])
@token_required
def update_department(current_user_payload, dept_id):
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求体不能为空"}), 400

    update_fields = []
    params = []
    if 'leader' in data:
        update_fields.append("leader = %s")
        params.append(data['leader'])
    if 'parentId' in data: # 注意检查 parentId 是否存在且不导致循环
        update_fields.append("parentId = %s")
        params.append(data.get('parentId')) # parentId can be null
    if 'name' in data: # 假设名称也可以修改
        update_fields.append("name = %s")
        params.append(data['name'])

    if not update_fields:
        return jsonify({"code": 400, "message": "没有提供可更新的字段"}), 400

    update_fields.append("updateAt = NOW()")
    params.append(dept_id)
    sql = f"UPDATE departments SET {', '.join(update_fields)} WHERE id = %s"

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        conn.commit()
        if cursor.rowcount > 0:
            return jsonify({"code": 0, "data": "更新部门成功"}), 200
        else:
            return jsonify({"code": 404, "message": "部门不存在或数据未更改"}), 404
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Update department error: {e}")
        return jsonify({"code": 500, "message": f"更新部门失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@bp.route('/department/<int:dept_id>', methods=['GET'])
@token_required
def get_department(current_user_payload, dept_id):
    """获取某个部门的信息, 严格按照Postman响应"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT id, name, parentId, leader, createAt, updateAt FROM departments WHERE id = %s"
        cursor.execute(sql, (dept_id,))
        department = cursor.fetchone()
        if department:
            # 格式化日期
            department['createAt'] = department['createAt'].isoformat() + "Z" if department['createAt'] else None
            department['updateAt'] = department['updateAt'].isoformat() + "Z" if department['updateAt'] else None
            return jsonify({"code": 0, "data": department}), 200
        else:
            return jsonify({"code": 404, "message": "部门不存在"}), 404
    except Exception as e:
        current_app.logger.error(f"Get department error: {e}")
        return jsonify({"code": 500, "message": f"查询部门失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# 注意：Postman文档中"获取部门列表"的示例是一个 GET /department/4 并带请求体，这不标准。
# 通常列表接口会是 GET /department/list (带查询参数) 或 POST /department/list (带请求体)。
# 这里我们实现一个 POST /department/list 以匹配 Postman 中其他列表接口的风格。
# 如果严格按照文档的 GET /department/:id 且可以带 body 来分页，那 get_department 需要修改。
# 这里假设列表接口是 POST /department/list，如果需要GET /department (无ID)来获取列表，则需另行实现。

@bp.route('/department/list', methods=['POST']) # 假设是POST请求获取列表
@token_required
def get_department_list(current_user_payload):
    """获取部门列表 (假设分页和筛选通过请求体)"""
    data = request.get_json() if request.data else {} # 允许空请求体
    offset = data.get('offset', 0)
    size = data.get('size', 10) # 默认每页10条
    # 可以添加 name, leader 等筛选条件
    name_filter = data.get('name')

    sql_offset = int(offset)
    sql_limit = int(size)

    params = []
    where_clauses = []
    if name_filter:
        where_clauses.append("name LIKE %s")
        params.append(f"%{name_filter}%")

    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        count_sql = f"SELECT COUNT(*) as totalCount FROM departments {where_sql}"
        cursor.execute(count_sql, tuple(params))
        total_count_result = cursor.fetchone()
        total_count = total_count_result['totalCount'] if total_count_result else 0

        list_sql = f"""
            SELECT id, name, parentId, leader, createAt, updateAt 
            FROM departments 
            {where_sql} 
            ORDER BY id ASC
            LIMIT %s, %s
        """

        final_params_for_list = list(params)
        final_params_for_list.append(sql_offset)
        final_params_for_list.append(sql_limit)

        cursor.execute(list_sql, tuple(final_params_for_list))
        departments = rows_to_list_of_dicts(cursor.fetchall()) # 使用辅助函数转换

        return jsonify({
            "code": 0,
            "data": {
                "list": departments,
                "totalCount": total_count
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get department list error: {e}")
        return jsonify({"code": 500, "message": f"查询部门列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# --- 角色管理 ---
@bp.route('/role', methods=['POST'])
@token_required
def create_role(current_user_payload):
    data = request.get_json()
    if not data or not data.get('name') or not data.get('intro'): # menuList is optional for creation based on some systems
        return jsonify({"code": 400, "message": "角色名称和介绍不能为空"}), 400

    menu_list_ids = data.get('menuList', []) # 菜单ID列表

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 检查角色名是否已存在
        cursor.execute("SELECT id FROM roles WHERE name = %s", (data['name'],))
        if cursor.fetchone():
            return jsonify({"code": 409, "message": "角色名称已存在"}), 409

        # 1. 创建角色
        sql_role = "INSERT INTO roles (name, intro, createAt, updateAt) VALUES (%s, %s, NOW(), NOW())"
        cursor.execute(sql_role, (data['name'], data['intro']))
        role_id = cursor.lastrowid # 获取新创建的角色ID

        # 2. 如果有 menuList, 则分配权限
        if role_id and menu_list_ids:
            # 先清除该角色可能存在的旧权限（对于新创建的角色非必需，但更新时常用）
            # cursor.execute("DELETE FROM role_menu WHERE role_id = %s", (role_id,))
            sql_role_menu = "INSERT INTO role_menu (role_id, menu_id) VALUES (%s, %s)"
            menu_tuples = [(role_id, menu_id) for menu_id in menu_list_ids]
            if menu_tuples: # 确保 menu_tuples 不为空
                cursor.executemany(sql_role_menu, menu_tuples)

        conn.commit()
        # 接口文档响应 "创建角色成功~"
        return jsonify({"code": 0, "data": "创建角色成功~"}), 201
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create role error: {e}")
        return jsonify({"code": 500, "message": f"创建角色失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/<int:role_id>', methods=['GET'])
@token_required
def get_role(current_user_payload, role_id):
    """获取单个角色信息"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 获取角色基本信息
        cursor.execute("SELECT id, name, intro, createAt, updateAt FROM roles WHERE id = %s", (role_id,))
        role = cursor.fetchone()
        
        if not role:
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 格式化日期
        role['createAt'] = role['createAt'].isoformat() + "Z" if role['createAt'] else None
        role['updateAt'] = role['updateAt'].isoformat() + "Z" if role['updateAt'] else None
        
        # 获取角色菜单列表
        cursor.execute("SELECT menu_id FROM role_menu WHERE role_id = %s", (role_id,))
        menu_ids = [row['menu_id'] for row in cursor.fetchall()]
        
        # 获取所有菜单项
        cursor.execute("SELECT id, name, type, url, icon, sort, parentId, permission, createAt, updateAt FROM menus ORDER BY sort ASC, id ASC")
        all_menus_flat = cursor.fetchall()
        
        # 构建菜单树
        def build_menu_tree(flat_menus, parent_id, role_menu_ids_set):
            branch = []
            for menu_item_flat in flat_menus:
                if menu_item_flat['id'] not in role_menu_ids_set:
                    continue
                if menu_item_flat['parentId'] == parent_id:
                    children = build_menu_tree(flat_menus, menu_item_flat['id'], role_menu_ids_set)
                    menu_node = dict(menu_item_flat)
                    menu_node['createAt'] = menu_node['createAt'].isoformat() + "Z" if menu_node['createAt'] else None
                    menu_node['updateAt'] = menu_node['updateAt'].isoformat() + "Z" if menu_node['updateAt'] else None
                    if children:
                        menu_node['children'] = children
                    else:
                        menu_node['children'] = [] if menu_item_flat['type'] != 3 else None
                    branch.append(menu_node)
            return branch if branch else None
        
        # 构建菜单树
        role_menu_ids_set = set(menu_ids)
        role_menu_list_tree = build_menu_tree(all_menus_flat, None, role_menu_ids_set) or []
        
        # 组装响应
        response_data = {
            "id": role['id'],
            "name": role['name'],
            "intro": role['intro'],
            "createAt": role['createAt'],
            "updateAt": role['updateAt'],
            "menuList": role_menu_list_tree
        }
        
        return jsonify({"code": 0, "data": response_data}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get role error: {e}")
        return jsonify({"code": 500, "message": f"获取角色信息失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/<int:role_id>', methods=['DELETE'])
@token_required
def delete_role(current_user_payload, role_id):
    """删除角色"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查角色是否存在
        cursor.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 检查是否有用户关联此角色
        cursor.execute("SELECT id FROM users WHERE role_id = %s LIMIT 1", (role_id,))
        if cursor.fetchone():
            return jsonify({"code": 400, "message": "该角色已被用户使用，无法删除"}), 400
        
        # 删除角色菜单关联记录
        cursor.execute("DELETE FROM role_menu WHERE role_id = %s", (role_id,))
        
        # 删除角色
        cursor.execute("DELETE FROM roles WHERE id = %s", (role_id,))
        
        conn.commit()
        return jsonify({"code": 0, "data": "删除角色成功"}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Delete role error: {e}")
        return jsonify({"code": 500, "message": f"删除角色失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/<int:role_id>', methods=['PATCH'])
@token_required
def update_role(current_user_payload, role_id):
    """修改角色"""
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求体不能为空"}), 400
    
    update_fields = []
    params = []
    
    if 'name' in data:
        update_fields.append("name = %s")
        params.append(data['name'])
    if 'intro' in data:
        update_fields.append("intro = %s")
        params.append(data['intro'])
    
    if not update_fields:
        return jsonify({"code": 400, "message": "没有提供可更新的字段"}), 400
    
    update_fields.append("updateAt = NOW()")
    params.append(role_id)
    
    sql = f"UPDATE roles SET {', '.join(update_fields)} WHERE id = %s"
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查角色是否存在
        cursor.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 更新角色
        cursor.execute(sql, tuple(params))
        
        # 如果提供了菜单列表，更新角色菜单关联
        if 'menuList' in data:
            menu_ids = data['menuList']
            # 清除原有权限
            cursor.execute("DELETE FROM role_menu WHERE role_id = %s", (role_id,))
            # 分配新权限
            if menu_ids:
                sql_role_menu = "INSERT INTO role_menu (role_id, menu_id) VALUES (%s, %s)"
                menu_tuples = [(role_id, menu_id) for menu_id in menu_ids]
                cursor.executemany(sql_role_menu, menu_tuples)
        
        conn.commit()
        return jsonify({"code": 0, "data": "修改角色成功"}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Update role error: {e}")
        return jsonify({"code": 500, "message": f"修改角色失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# GET /role/:id/menu (查询角色菜单树 - 这是一个较复杂的查询，需要递归或多次查询构建树)
# GET /role/:id/menuIds (查询角色菜单ID列表)
# POST /role/assign (给角色分配权限)

# 我将提供 /role/list 的一个简化版本作为示例
@bp.route('/role/list', methods=['POST'])
@token_required
def get_role_list(current_user_payload):
    """获取角色列表 (严格按照Postman响应体结构)"""
    data = request.get_json() if request.data else {}
    offset = data.get('offset', 0)
    size = data.get('size', 10)

    sql_offset = int(offset)
    sql_limit = int(size)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. 获取角色总数
        cursor.execute("SELECT COUNT(*) as totalCount FROM roles")
        total_count = cursor.fetchone()['totalCount']

        # 2. 获取分页后的角色基本信息
        sql_roles = "SELECT id, name, intro, createAt, updateAt FROM roles ORDER BY id ASC LIMIT %s, %s"
        cursor.execute(sql_roles, (sql_offset, sql_limit))
        roles_data = cursor.fetchall()

        result_list = []
        for role in roles_data:
            # 3. 为每个角色获取其 menuList (这是一个复杂操作，理想情况下应优化)
            # 这里简化为获取 menu_id 列表，然后查询所有相关的 menu项，再构建树
            # 严格按照 Postman 响应，menuList 是一个包含完整菜单对象的树状结构

            # 获取该角色的所有菜单ID
            cursor.execute("SELECT menu_id FROM role_menu WHERE role_id = %s", (role['id'],))
            menu_ids_for_role = [row['menu_id'] for row in cursor.fetchall()]

            role_menu_list_tree = []
            if menu_ids_for_role:
                # 构建菜单树是一个复杂的过程，这里仅做示意
                # 实际中需要一个辅助函数来从扁平的菜单列表和父子关系构建树
                # 并且只包含该角色拥有的菜单项
                # 简化：查询这些ID对应的菜单项，并尝试构建第一层 (不完全符合Postman的嵌套结构)

                # 为了演示，我们先获取所有菜单项，然后在应用层过滤和构建树
                # 这不是最高效的方式，但能模拟响应结构
                cursor.execute("SELECT id, name, type, url, icon, sort, parentId, permission, createAt, updateAt FROM menus ORDER BY sort ASC, id ASC")
                all_menus_flat = cursor.fetchall()

                # 辅助函数来构建树 (非常简化版，且未过滤角色权限)
                # 实际中，这个函数会复杂得多，需要递归，并且只选择 role_menu_ids 中的菜单
                def build_menu_tree_for_role(flat_menus, parent_id, role_menu_ids_set):
                    branch = []
                    for menu_item_flat in flat_menus:
                        if menu_item_flat['id'] not in role_menu_ids_set: # 只包含角色有的菜单
                            continue
                        if menu_item_flat['parentId'] == parent_id:
                            children = build_menu_tree_for_role(flat_menus, menu_item_flat['id'], role_menu_ids_set)
                            menu_node = dict(menu_item_flat) # copy
                            menu_node['createAt'] = menu_node['createAt'].isoformat() + "Z" if menu_node['createAt'] else None
                            menu_node['updateAt'] = menu_node['updateAt'].isoformat() + "Z" if menu_node['updateAt'] else None
                            if children:
                                menu_node['children'] = children
                            else:
                                # Postman响应中，即使type 2没有子权限按钮，children也可能是空数组或null
                                # type 3 (button) children is null
                                menu_node['children'] = [] if menu_item_flat['type'] != 3 else None
                            branch.append(menu_node)
                    return branch if branch else None # 如果没有子项，返回None或空列表，根据接口而定

                role_menu_ids_set = set(menu_ids_for_role)
                role_menu_list_tree = build_menu_tree_for_role(all_menus_flat, None, role_menu_ids_set) or []


            result_list.append({
                "id": role['id'],
                "name": role['name'],
                "intro": role['intro'],
                "createAt": role['createAt'].isoformat() + "Z" if role['createAt'] else None,
                "updateAt": role['updateAt'].isoformat() + "Z" if role['updateAt'] else None,
                "menuList": role_menu_list_tree # 这里应该是构建好的树形菜单列表
            })

        return jsonify({
            "code": 0,
            "data": {
                "list": result_list,
                "totalCount": total_count
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Get role list error: {e}")
        return jsonify({"code": 500, "message": f"查询角色列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# --- 菜单管理 ---
@bp.route('/menu', methods=['POST'])
@token_required
def create_menu(current_user_payload):
    """创建菜单"""
    data = request.get_json()
    if not data or not data.get('name') or not data.get('type'):
        return jsonify({"code": 400, "message": "菜单名称和类型不能为空"}), 400
    
    # 必要字段
    menu_type = data.get('type')
    name = data.get('name')
    
    # 可选字段
    url = data.get('url', '')
    icon = data.get('icon', '')
    permission = data.get('permission', '')
    parent_id = data.get('parentId')
    sort = data.get('sort', 100)  # 默认排序值
    
    # 根据类型验证字段
    if menu_type == 1:  # 目录
        if not icon:
            return jsonify({"code": 400, "message": "目录类型菜单需要提供图标"}), 400
    elif menu_type == 2:  # 菜单
        if not url:
            return jsonify({"code": 400, "message": "菜单类型需要提供URL"}), 400
    elif menu_type == 3:  # 按钮/权限
        if not permission:
            return jsonify({"code": 400, "message": "按钮/权限类型需要提供权限标识"}), 400
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 如果有父ID，验证父菜单是否存在
        if parent_id:
            cursor.execute("SELECT id, type FROM menus WHERE id = %s", (parent_id,))
            parent = cursor.fetchone()
            if not parent:
                return jsonify({"code": 404, "message": "父菜单不存在"}), 404
                
            # 验证父子关系是否合法
            if parent['type'] == 3:  # 按钮不能作为父菜单
                return jsonify({"code": 400, "message": "按钮类型不能作为父菜单"}), 400
                
            if menu_type < parent['type']:  # 子类型必须大于等于父类型
                return jsonify({"code": 400, "message": "子菜单类型必须大于等于父菜单类型"}), 400
        
        # 插入菜单
        sql = """
            INSERT INTO menus (name, type, url, icon, sort, parentId, permission, createAt, updateAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(sql, (name, menu_type, url, icon, sort, parent_id, permission))
        conn.commit()
        
        return jsonify({"code": 0, "data": {"id": cursor.lastrowid, "message": "创建菜单成功"}}), 201
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create menu error: {e}")
        return jsonify({"code": 500, "message": f"创建菜单失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/menu/<int:menu_id>', methods=['GET'])
@token_required
def get_menu(current_user_payload, menu_id):
    """获取单个菜单信息"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, type, url, icon, sort, parentId, permission, createAt, updateAt FROM menus WHERE id = %s", (menu_id,))
        menu = cursor.fetchone()
        
        if not menu:
            return jsonify({"code": 404, "message": "菜单不存在"}), 404
        
        # 格式化日期
        menu['createAt'] = menu['createAt'].isoformat() + "Z" if menu['createAt'] else None
        menu['updateAt'] = menu['updateAt'].isoformat() + "Z" if menu['updateAt'] else None
        
        return jsonify({"code": 0, "data": menu}), 200
        
    except Exception as e:
        current_app.logger.error(f"Get menu error: {e}")
        return jsonify({"code": 500, "message": f"获取菜单信息失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/menu/<int:menu_id>', methods=['PATCH'])
@token_required
def update_menu(current_user_payload, menu_id):
    """修改菜单"""
    data = request.get_json()
    if not data:
        return jsonify({"code": 400, "message": "请求体不能为空"}), 400
    
    update_fields = []
    params = []
    
    if 'name' in data:
        update_fields.append("name = %s")
        params.append(data['name'])
    if 'type' in data:
        update_fields.append("type = %s")
        params.append(data['type'])
    if 'url' in data:
        update_fields.append("url = %s")
        params.append(data['url'])
    if 'icon' in data:
        update_fields.append("icon = %s")
        params.append(data['icon'])
    if 'sort' in data:
        update_fields.append("sort = %s")
        params.append(data['sort'])
    if 'permission' in data:
        update_fields.append("permission = %s")
        params.append(data['permission'])
    if 'parentId' in data:
        update_fields.append("parentId = %s")
        params.append(data['parentId'])
    
    if not update_fields:
        return jsonify({"code": 400, "message": "没有提供可更新的字段"}), 400
    
    update_fields.append("updateAt = NOW()")
    params.append(menu_id)
    
    sql = f"UPDATE menus SET {', '.join(update_fields)} WHERE id = %s"
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查菜单是否存在
        cursor.execute("SELECT id FROM menus WHERE id = %s", (menu_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "菜单不存在"}), 404
        
        # 如果更新了父ID，验证父菜单是否存在
        if 'parentId' in data and data['parentId']:
            cursor.execute("SELECT id, type FROM menus WHERE id = %s", (data['parentId'],))
            parent = cursor.fetchone()
            if not parent:
                return jsonify({"code": 404, "message": "父菜单不存在"}), 404
                
            # 验证父子关系是否合法
            if parent['type'] == 3:  # 按钮不能作为父菜单
                return jsonify({"code": 400, "message": "按钮类型不能作为父菜单"}), 400
                
            # 验证菜单类型
            if 'type' in data:
                if data['type'] < parent['type']:  # 子类型必须大于等于父类型
                    return jsonify({"code": 400, "message": "子菜单类型必须大于等于父菜单类型"}), 400
            else:
                cursor.execute("SELECT type FROM menus WHERE id = %s", (menu_id,))
                menu_type = cursor.fetchone()['type']
                if menu_type < parent['type']:
                    return jsonify({"code": 400, "message": "子菜单类型必须大于等于父菜单类型"}), 400
            
            # 防止循环引用
            if data['parentId'] == menu_id:
                return jsonify({"code": 400, "message": "菜单不能作为自己的父菜单"}), 400
            
            # 检查子菜单路径
            cursor.execute("WITH RECURSIVE menu_path (id, path) AS (SELECT id, CAST(id AS CHAR(200)) FROM menus WHERE id = %s UNION ALL SELECT m.id, CONCAT(mp.path, ',', m.id) FROM menus m JOIN menu_path mp ON m.parentId = mp.id) SELECT path FROM menu_path WHERE id = %s", (data['parentId'], menu_id))
            if cursor.fetchone():
                return jsonify({"code": 400, "message": "不能将菜单的子菜单设为其父菜单（循环引用）"}), 400
        
        cursor.execute(sql, tuple(params))
        conn.commit()
        
        return jsonify({"code": 0, "data": "修改菜单成功"}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Update menu error: {e}")
        return jsonify({"code": 500, "message": f"修改菜单失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/menu/<int:menu_id>', methods=['DELETE'])
@token_required
def delete_menu(current_user_payload, menu_id):
    """删除菜单"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查菜单是否存在
        cursor.execute("SELECT id FROM menus WHERE id = %s", (menu_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "菜单不存在"}), 404
        
        # 检查是否有子菜单
        cursor.execute("SELECT id FROM menus WHERE parentId = %s LIMIT 1", (menu_id,))
        if cursor.fetchone():
            return jsonify({"code": 400, "message": "该菜单有子菜单，无法删除"}), 400
        
        # 检查是否有角色关联
        cursor.execute("SELECT role_id FROM role_menu WHERE menu_id = %s LIMIT 1", (menu_id,))
        if cursor.fetchone():
            # 删除菜单角色关联
            cursor.execute("DELETE FROM role_menu WHERE menu_id = %s", (menu_id,))
        
        # 删除菜单
        cursor.execute("DELETE FROM menus WHERE id = %s", (menu_id,))
        
        conn.commit()
        return jsonify({"code": 0, "data": "删除菜单成功"}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Delete menu error: {e}")
        return jsonify({"code": 500, "message": f"删除菜单失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/menu/list', methods=['POST']) # Postman是POST
@token_required
def get_all_menus_tree(current_user_payload):
    """查询完整菜单树"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 获取所有菜单项，按 sort 和 id 排序以帮助构建树
        cursor.execute("""
            SELECT id, name, type, url, icon, sort, parentId, permission, createAt, updateAt 
            FROM menus 
            ORDER BY parentId ASC, sort ASC, id ASC
        """)
        all_menus_flat = cursor.fetchall()

        # 构建树形结构
        menu_map = {menu['id']: menu for menu in all_menus_flat}
        tree = []
        for menu_item_flat in all_menus_flat:
            # 格式化日期
            menu_item_flat['createAt'] = menu_item_flat['createAt'].isoformat() + "Z" if menu_item_flat['createAt'] else None
            menu_item_flat['updateAt'] = menu_item_flat['updateAt'].isoformat() + "Z" if menu_item_flat['updateAt'] else None

            menu_item_flat['children'] = [] # 初始化 children 列表

            if menu_item_flat['parentId'] is None:
                tree.append(menu_item_flat)
            else:
                parent = menu_map.get(menu_item_flat['parentId'])
                if parent:
                    # Postman响应中，即使type 2没有子权限按钮，children也可能是空数组或null
                    # type 3 (button) children is null
                    # 为了准确模仿，这里需要更细致的逻辑，如果一个type=2的项没有子（type=3）项，children应为空数组。
                    # 如果一个type=1/2的项就是叶子节点（没有子菜单），children也应是空数组。
                    # 如果是type=3的按钮，Postman响应中其children字段为null。
                    if menu_item_flat['type'] == 3:
                        menu_item_flat['children'] = None # 按钮权限没有子节点

                    parent['children'].append(menu_item_flat)

        # 清理 children 为空的 Type 1/2 节点的 children 字段，如果 Postman 响应是 null 而不是 []
        # (根据 Postman /menu/list 响应，叶子节点的 children 是 null 或空数组，按钮是 null)
        def finalize_children(node):
            if node.get('children') is not None: # 不是按钮
                if not node['children']: # 如果是空列表
                    if node['type'] == 1 or node['type'] == 2: # 目录或菜单
                        node['children'] = None # Postman 示例中叶子节点 children 为 null
                else:
                    for child in node['children']:
                        finalize_children(child)

        for root_node in tree:
            finalize_children(root_node)

        return jsonify({"code": 0, "data": {"list": tree}}), 200

    except Exception as e:
        current_app.logger.error(f"Get all menus tree error: {e}")
        return jsonify({"code": 500, "message": f"查询菜单树失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/<int:role_id>/menu', methods=['GET'])
@token_required
def get_role_menu(current_user_payload, role_id):
    """获取角色菜单权限"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 首先检查角色是否存在
        cursor.execute("SELECT id, name FROM roles WHERE id = %s", (role_id,))
        role = cursor.fetchone()
        if not role:
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 获取所有菜单项
        cursor.execute("SELECT * FROM menus ORDER BY type, sort")
        all_menus_flat = cursor.fetchall()
        
        # 获取角色的菜单权限
        cursor.execute("SELECT menu_id FROM role_menu WHERE role_id = %s", (role_id,))
        menu_ids_for_role = [row['menu_id'] for row in cursor.fetchall()]
        role_menu_ids_set = set(menu_ids_for_role)
        
        # 构建菜单树
        def build_menu_tree(flat_menus, parent_id=None):
            tree = []
            for menu_item in flat_menus:
                if menu_item['parentId'] == parent_id and menu_item['id'] in role_menu_ids_set:
                    # 深拷贝当前菜单项
                    menu_node = dict(menu_item)
                    # 递归构建子菜单
                    children = build_menu_tree(flat_menus, menu_item['id'])
                    if children:
                        menu_node['children'] = children
                    tree.append(menu_node)
            return tree
        
        # 构建菜单树
        menu_tree = build_menu_tree(all_menus_flat)
        
        return jsonify({
            "code": 0,
            "data": menu_tree
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get role menu error: {e}")
        return jsonify({"code": 500, "message": f"获取角色菜单失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/<int:role_id>/menuIds', methods=['GET'])
@token_required
def get_role_menu_ids(current_user_payload, role_id):
    """获取角色菜单ID列表"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查角色是否存在
        cursor.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 获取角色的菜单ID列表
        cursor.execute("SELECT menu_id FROM role_menu WHERE role_id = %s", (role_id,))
        menu_ids = [row['menu_id'] for row in cursor.fetchall()]
        
        return jsonify({
            "code": 0,
            "data": menu_ids
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get role menu IDs error: {e}")
        return jsonify({"code": 500, "message": f"获取角色菜单ID列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/role/assign', methods=['POST'])
@token_required
def assign_role_menu(current_user_payload):
    """给角色分配权限"""
    data = request.get_json()
    if not data or 'roleId' not in data or 'menuIds' not in data:
        return jsonify({"code": 400, "message": "缺少必要参数"}), 400
    
    role_id = data['roleId']
    menu_ids = data['menuIds']
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 检查角色是否存在
        cursor.execute("SELECT id FROM roles WHERE id = %s", (role_id,))
        if not cursor.fetchone():
            return jsonify({"code": 404, "message": "角色不存在"}), 404
        
        # 清除原有权限
        cursor.execute("DELETE FROM role_menu WHERE role_id = %s", (role_id,))
        
        # 分配新权限
        if menu_ids:
            sql_role_menu = "INSERT INTO role_menu (role_id, menu_id) VALUES (%s, %s)"
            menu_tuples = [(role_id, menu_id) for menu_id in menu_ids]
            cursor.executemany(sql_role_menu, menu_tuples)
        
        conn.commit()
        return jsonify({"code": 0, "data": "角色权限分配成功"}), 200
        
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Assign role menu error: {e}")
        return jsonify({"code": 500, "message": f"角色权限分配失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()