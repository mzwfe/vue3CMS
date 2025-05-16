# vue3CMS-backend/app/routes/product_management.py
from flask import Blueprint, request, jsonify, current_app
import pymysql
import traceback
from app.utils.auth_utils import token_required
from datetime import datetime
from app.config import get_config

bp = Blueprint('product_management', __name__)

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

def row_to_dict_product(row):
    if row is None:
        return None
    d = dict(row)
    for key, value in d.items():
        if isinstance(value, datetime):
            d[key] = value.isoformat() + 'Z'
        # 根据接口文档，价格是字符串
        if key in ['oldPrice', 'newPrice'] and value is not None:
            d[key] = str(value) # 确保是字符串
    return d

def rows_to_list_of_dicts_product(rows):
    return [row_to_dict_product(row) for row in rows]

# --- 商品分类管理 ---
@bp.route('/category', methods=['POST'])
@token_required
def create_category(current_user_payload):
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"code": 400, "message": "分类名称不能为空"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 检查分类名是否已存在
        cursor.execute("SELECT id FROM categories WHERE name = %s", (data['name'],))
        if cursor.fetchone():
            return jsonify({"code": 409, "message": "分类名称已存在"}), 409

        sql = "INSERT INTO categories (name, createAt, updateAt) VALUES (%s, NOW(), NOW())"
        cursor.execute(sql, (data['name'],))
        conn.commit()
        # 接口文档响应 "创建商品类别成功~"
        return jsonify({"code": 0, "data": "创建商品类别成功~"}), 201
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create category error: {e}")
        return jsonify({"code": 500, "message": f"创建分类失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/category/list', methods=['POST'])
@token_required
def get_category_list(current_user_payload):
    data = request.get_json() if request.data else {}
    offset = data.get('offset', 0)
    size = data.get('size', 10)
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
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()

        count_sql = f"SELECT COUNT(*) as totalCount FROM categories {where_sql}"
        cursor.execute(count_sql, tuple(params))
        total_count = cursor.fetchone()['totalCount']

        list_sql = f"SELECT id, name, createAt, updateAt FROM categories {where_sql} ORDER BY id DESC LIMIT %s, %s"

        final_params_for_list = list(params)
        final_params_for_list.append(sql_offset)
        final_params_for_list.append(sql_limit)

        cursor.execute(list_sql, tuple(final_params_for_list))
        categories = rows_to_list_of_dicts_product(cursor.fetchall())

        return jsonify({
            "code": 0,
            "data": {
                "list": categories,
                "totalCount": total_count
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get category list error: {e}")
        return jsonify({"code": 500, "message": f"查询分类列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# --- 商品信息管理 ---
@bp.route('/goods', methods=['POST'])
@token_required
def create_product(current_user_payload):
    data = request.get_json()
    # 根据文档，这些字段是必须的
    required_fields = ['name', 'oldPrice', 'newPrice', 'desc', 'status', 'imgUrl', 'inventoryCount', 'saleCount', 'favorCount', 'address']
    if not all(field in data for field in required_fields):
        return jsonify({"code": 400, "message": "缺少必要的商品信息"}), 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO products 
            (name, oldPrice, newPrice, `desc`, status, imgUrl, inventoryCount, saleCount, favorCount, address, categoryId, createAt, updateAt) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
        """
        # 注意 `desc` 是 SQL 关键字，需要用反引号括起来
        cursor.execute(sql, (
            data['name'], str(data['oldPrice']), str(data['newPrice']), data['desc'], data['status'], data['imgUrl'],
            data['inventoryCount'], data['saleCount'], data['favorCount'], data['address'], data.get('categoryId') # categoryId can be null
        ))
        conn.commit()
        return jsonify({"code": 0, "data": "创建商品成功~"}), 201
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create product error: {e}")
        return jsonify({"code": 500, "message": f"创建商品失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/list', methods=['POST']) # 文档中是 POST
@token_required
def get_product_list(current_user_payload):
    data = request.get_json() if request.data else {} # 允许空请求体，表示获取全部（带分页）
    offset = data.get('offset', 0) # 假设offset是SQL的跳过数量
    size = data.get('size', 10)
    # 可以添加筛选条件，如 name, categoryId, status等，但文档请求体为空

    sql_offset = int(offset)
    sql_limit = int(size)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()

        # 获取总数
        cursor.execute("SELECT COUNT(*) as totalCount FROM products")
        total_count = cursor.fetchone()['totalCount']

        # 获取商品列表
        sql_products = """
            SELECT id, name, oldPrice, newPrice, `desc`, status, imgUrl, 
                   inventoryCount, saleCount, favorCount, address, categoryId, 
                   createAt, updateAt 
            FROM products 
            ORDER BY id DESC 
            LIMIT %s, %s
        """
        cursor.execute(sql_products, (sql_offset, sql_limit))
        products_list = rows_to_list_of_dicts_product(cursor.fetchall())

        return jsonify({
            "code": 0,
            "data": {
                "list": products_list,
                "totalCount": total_count
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get product list error: {e}")
        return jsonify({"code": 500, "message": f"查询商品列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


# ... (其他商品、分类的 DELETE, PATCH, GET /resource/:id 接口实现)
# GET /goods/:id 的响应在 Postman 中只有 {"code": 0}，这里我们返回完整商品信息
@bp.route('/goods/<int:product_id>', methods=['GET'])
@token_required
def get_product_detail(current_user_payload, product_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        sql = """
            SELECT id, name, oldPrice, newPrice, `desc`, status, imgUrl, 
                   inventoryCount, saleCount, favorCount, address, categoryId, 
                   createAt, updateAt 
            FROM products 
            WHERE id = %s
        """
        cursor.execute(sql, (product_id,))
        product = row_to_dict_product(cursor.fetchone())

        if product:
            return jsonify({"code": 0, "data": product}), 200
        else:
            # 严格按Postman文档，如果找不到也可能只返回 code: 0，但通常会是404
            # return jsonify({"code": 0}), 200 # 严格按Postman示例的响应体 (即使找不到)
            return jsonify({"code": 404, "message": "商品不存在"}), 404
    except Exception as e:
        current_app.logger.error(f"Get product detail error: {e}")
        return jsonify({"code": 500, "message": f"查询商品详情失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()