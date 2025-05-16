# vue3CMS-backend/app/routes/chart.py
from flask import Blueprint, jsonify, current_app
import pymysql
import traceback
from app.utils.auth_utils import token_required
from datetime import datetime
from app.config import get_config

bp = Blueprint('chart', __name__)

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

def row_to_dict_chart(row):
    if row is None:
        return None
    # 字典游标已经返回字典了
    d = dict(row)
    # 如果有日期字段需要特定格式化，可以在这里处理
    # 例如，如果createAt/updateAt出现在图表数据中
    for key, value in d.items():
        if isinstance(value, datetime):
            d[key] = value.isoformat() + 'Z'
    return d

def rows_to_list_of_dicts_chart(rows):
    return [row_to_dict_chart(row) for row in rows]

@bp.route('/goods/category/count', methods=['GET'])
@token_required
def get_goods_category_count(current_user_payload):
    """每个分类商品的个数"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # Postman 响应: {"id": 2, "name": "上衣", "goodsCount": 14}
        sql = """
            SELECT 
                c.id, 
                c.name, 
                COUNT(p.id) as goodsCount 
            FROM categories c 
            LEFT JOIN products p ON c.id = p.categoryId 
            GROUP BY c.id, c.name
            ORDER BY c.id ASC;
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        return jsonify({"code": 0, "data": data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods category count: {e}")
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/category/sale', methods=['GET'])
@token_required
def get_goods_category_sale(current_user_payload):
    """每个分类商品的销量"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # Postman 响应: {"id": 2, "name": "上衣", "goodsCount": 49749} (这里的goodsCount实际是销量)
        sql = """
            SELECT 
                c.id, 
                c.name, 
                SUM(p.saleCount) as goodsCount --  'goodsCount' is used in response for sum of sales
            FROM categories c 
            LEFT JOIN products p ON c.id = p.categoryId 
            GROUP BY c.id, c.name
            ORDER BY c.id ASC;
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        # Postman 响应中，如果某分类没有商品，goodsCount 为 null
        for item in data:
            if item['goodsCount'] is None: # SUM(NULL) might be NULL or 0 depending on DB and data
                pass # DB already returns NULL if no sales or all sales are NULL
        return jsonify({"code": 0, "data": data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods category sale: {e}")
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/category/favor', methods=['GET'])
@token_required
def get_goods_category_favor(current_user_payload):
    """每个分类商品的收藏"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # Postman 响应: {"id": 2, "name": "上衣", "goodsFavor": 6091}
        sql = """
            SELECT 
                c.id, 
                c.name, 
                SUM(p.favorCount) as goodsFavor 
            FROM categories c 
            LEFT JOIN products p ON c.id = p.categoryId 
            GROUP BY c.id, c.name
            ORDER BY c.id ASC;
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        return jsonify({"code": 0, "data": data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods category favor: {e}")
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/sale/top10', methods=['GET'])
@token_required
def get_goods_sale_top10(current_user_payload):
    """销量前10的商品数量"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # Postman 响应: {"id": 7, "name": "秋装女2018...", "saleCount": 32070}
        sql = """
            SELECT 
                p.id, 
                p.name, 
                p.saleCount
            FROM products p
            ORDER BY p.saleCount DESC
            LIMIT 10;
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        return jsonify({"code": 0, "data": data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods sale top10: {e}")
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/address/sale', methods=['GET'])
@token_required
def get_goods_address_sale(current_user_payload):
    """不同城市的销量数据"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        # Postman 响应: {"address": "上海", "count": 62239}
        sql = """
            SELECT 
                p.address, 
                SUM(p.saleCount) as count 
            FROM products p
            WHERE p.address IS NOT NULL AND p.address != '' 
            GROUP BY p.address
            ORDER BY count DESC; 
        """ # 确保address不为空
        cursor.execute(sql)
        data = cursor.fetchall()
        return jsonify({"code": 0, "data": data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods address sale: {e}")
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@bp.route('/goods/amount/list', methods=['GET'])
@token_required
def get_goods_amount_list(current_user_payload):
    """商品数据统计的数量"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()

        # 商品总销量
        cursor.execute("SELECT SUM(saleCount) as total_sales FROM products")
        total_sales = cursor.fetchone()['total_sales'] or 0

        # 商品总收藏
        cursor.execute("SELECT SUM(favorCount) as total_favors FROM products")
        total_favors = cursor.fetchone()['total_favors'] or 0

        # 商品总库存
        cursor.execute("SELECT SUM(inventoryCount) as total_inventory FROM products")
        total_inventory = cursor.fetchone()['total_inventory'] or 0

        # 商品总销售额 (newPrice * saleCount)
        cursor.execute("SELECT SUM(CAST(newPrice AS DECIMAL(10,2)) * saleCount) as total_revenue FROM products")
        total_revenue_result = cursor.fetchone()
        total_revenue = total_revenue_result['total_revenue'] if total_revenue_result and total_revenue_result['total_revenue'] is not None else 0.0


        response_data = [
            {
                "amount": "sale", "title": "商品总销量", "tips": "所有商品的总销量",
                "subtitle": "商品总销量", "number1": int(total_sales), "number2": int(total_sales)
            },
            {
                "amount": "favor", "title": "商品总收藏", "tips": "所有商品的总收藏",
                "subtitle": "商品总收藏", "number1": int(total_favors), "number2": int(total_favors)
            },
            {
                "amount": "inventory", "title": "商品总库存", "tips": "所有商品的总库存",
                "subtitle": "商品总库存", "number1": int(total_inventory), "number2": int(total_inventory)
            },
            {
                "amount": "saleroom", "title": "商品总销售额", "tips": "所有商品的总销售额",
                "subtitle": "商品总销售额", "number1": float(total_revenue), "number2": float(total_revenue) # 接口文档返回的是数字
            }
        ]
        return jsonify({"code": 0, "data": response_data}), 200
    except Exception as e:
        current_app.logger.error(f"Error getting goods amount list: {e}")
        return jsonify({"code": 500, "message": f"查询商品统计失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()