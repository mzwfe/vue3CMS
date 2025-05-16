# vue3CMS-backend/app/routes/story.py
from flask import Blueprint, request, jsonify, current_app
import pymysql
import traceback
from app.utils.auth_utils import token_required
from datetime import datetime
from app.config import get_config

bp = Blueprint('story', __name__)

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

def row_to_dict_story(row):
    if row is None:
        return None
    d = dict(row)
    if 'createAt' in d and isinstance(d['createAt'], datetime):
        d['createAt'] = d['createAt'].isoformat() + 'Z'
    return d

def rows_to_list_of_dicts_story(rows):
    return [row_to_dict_story(row) for row in rows]


@bp.route('/story', methods=['POST'])
@token_required
def create_story(current_user_payload):
    """创建故事"""
    data = request.get_json()
    if not data or not data.get('title') or data.get('content') is None: # content可以是空字符串
        return jsonify({"code": 400, "message": "标题和内容不能为空"}), 400

    title = data['title']
    content = data['content']
    user_id = current_user_payload.get('id') # 从token中获取用户ID

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"code": 500, "message": "数据库连接失败"}), 500
            
        cursor = conn.cursor()
        sql = "INSERT INTO stories (title, content, user_id, createAt) VALUES (%s, %s, %s, NOW())"
        cursor.execute(sql, (title, content, user_id))
        conn.commit()
        # Postman响应体: {"code": 0, "data": "创建故事成功~"}
        return jsonify({"code": 0, "data": "创建故事成功~"}), 201
    except Exception as e:
        if conn: conn.rollback()
        current_app.logger.error(f"Create story error: {e}")
        return jsonify({"code": 500, "message": f"创建故事失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@bp.route('/story/list', methods=['POST'])
@token_required
def get_story_list(current_user_payload):
    """获取故事列表"""
    data = request.get_json() if request.data else {}
    offset = data.get('offset', 0)
    size = data.get('size', 10) # 默认Postman中是3000，但这里用10作为通用分页默认值

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
        cursor.execute("SELECT COUNT(*) as totalCount FROM stories")
        total_count_result = cursor.fetchone()
        total_count = total_count_result['totalCount'] if total_count_result else 0

        # 获取故事列表 (Postman响应体中只包含id, title, content, createAt)
        sql_stories = "SELECT id, title, content, createAt FROM stories ORDER BY id DESC LIMIT %s, %s"
        cursor.execute(sql_stories, (sql_offset, sql_limit))
        stories_list = rows_to_list_of_dicts_story(cursor.fetchall())

        return jsonify({
            "code": 0,
            "data": {
                "list": stories_list,
                "totalCount": total_count
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Get story list error: {e}")
        return jsonify({"code": 500, "message": f"查询故事列表失败: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()