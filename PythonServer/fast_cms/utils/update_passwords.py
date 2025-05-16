#!/usr/bin/env python
# 更新数据库中现有用户的密码为加密形式
import pymysql
import sys
import os
import traceback

# 将fast_cms目录添加到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import get_config
from app.utils.auth_utils import hash_password
from flask import current_app

def get_db_connection():
    """使用pymysql方式获取数据库连接"""
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
        print(f"数据库连接错误: {e}")
        traceback.print_exc()
        return None

def is_bcrypt_hash(password_str):
    """判断是否为bcrypt格式的哈希"""
    return (password_str.startswith('$2a$') or 
            password_str.startswith('$2b$') or 
            password_str.startswith('pbkdf2:sha256:'))

def update_passwords():
    """更新所有用户密码为加密形式"""
    conn = get_db_connection()
    if not conn:
        print("数据库连接失败，无法继续")
        return

    try:
        cursor = conn.cursor()
        
        # 获取所有用户
        cursor.execute("SELECT id, name, password FROM users")
        users = cursor.fetchall()
        
        if not users:
            print("数据库中没有用户")
            return
            
        print(f"找到 {len(users)} 个用户账号")
        updated_count = 0
        skipped_count = 0
        
        for user in users:
            user_id = user['id']
            user_name = user['name']
            current_password = user['password']
            
            # 检查密码是否已经是加密形式
            if current_password and is_bcrypt_hash(current_password):
                print(f"用户 {user_name} (ID: {user_id}) 的密码已是加密形式，跳过")
                skipped_count += 1
                continue
            
            # 为纯文本密码创建加密形式
            # 这里使用默认密码"123456"
            print(f"处理用户 {user_name} (ID: {user_id}) 的密码...")
            
            # 如果密码是"hashed_password_placeholder_for_123456"这样的占位符
            if current_password and "placeholder" in current_password.lower():
                print(f"  检测到密码占位符，假设实际密码为123456")
                default_password = "123456"
            else:
                # 否则使用默认密码或当前值
                default_password = "123456" if not current_password else current_password
                print(f"  使用{'默认密码123456' if not current_password else '当前存储的密码值'}")
            
            try:
                hashed_password = hash_password(default_password)
                
                # 更新用户的密码
                cursor.execute(
                    "UPDATE users SET password = %s WHERE id = %s",
                    (hashed_password, user_id)
                )
                updated_count += 1
                print(f"  ✓ 已更新用户 {user_name} (ID: {user_id}) 的密码为加密形式")
            except Exception as e:
                print(f"  ✗ 处理用户 {user_name} (ID: {user_id}) 的密码时出错: {e}")
                continue
        
        # 提交所有更改
        conn.commit()
        print(f"\n密码更新完成: 更新 {updated_count} 个，跳过 {skipped_count} 个")
        
    except Exception as e:
        conn.rollback()
        print(f"更新密码时出错: {e}")
        traceback.print_exc()
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

if __name__ == "__main__":
    print("开始更新用户密码...")
    update_passwords()
    print("操作完成") 