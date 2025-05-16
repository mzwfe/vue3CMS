#!/usr/bin/env python
# 测试用户登录和信息获取
import requests
import json
import sys
import os
import pymysql.cursors

# 将fast_cms目录添加到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import get_config

# API基础URL
BASE_URL = "http://localhost:5000/api"  # 根据实际情况调整

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
        return None

def show_all_users():
    """显示数据库中所有用户的信息（不包括密码）"""
    conn = get_db_connection()
    if not conn:
        print("数据库连接失败，无法显示用户信息")
        return
    
    try:
        cursor = conn.cursor()
        query = """
        SELECT u.id, u.name, u.realname, u.cellphone, u.enable, 
               r.name as role_name, d.name as department_name
        FROM users u
        LEFT JOIN roles r ON u.role_id = r.id
        LEFT JOIN departments d ON u.department_id = d.id
        """
        cursor.execute(query)
        users = cursor.fetchall()
        
        if not users:
            print("数据库中没有用户记录")
            return
        
        print("\n=== 数据库中的用户信息 ===")
        print("ID\t用户名\t真实姓名\t电话\t\t状态\t角色\t\t部门")
        print("-" * 100)
        
        for user in users:
            status = "启用" if user["enable"] else "禁用"
            print(f"{user['id']}\t{user['name']}\t{user['realname'] or 'N/A'}\t{user['cellphone'] or 'N/A'}\t{status}\t{user['role_name'] or 'N/A'}\t{user['department_name'] or 'N/A'}")
            
    except Exception as e:
        print(f"查询用户时出错: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()

def login(username, password):
    """登录并获取token"""
    login_url = f"{BASE_URL}/login"
    
    login_data = {
        "name": username,
        "password": password
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("code") == 0:
            token = response_data["data"]["token"]
            user_id = response_data["data"]["id"]
            print(f"登录成功！用户ID: {user_id}, 用户名: {username}")
            return token
        else:
            print(f"登录失败: {response_data.get('message', '未知错误')}")
            return None
    except Exception as e:
        print(f"登录请求出错: {e}")
        return None

def get_user_info(token):
    """使用token获取用户详细信息"""
    if not token:
        print("没有有效的token，无法获取用户信息")
        return
    
    user_info_url = f"{BASE_URL}/user_info"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(user_info_url, headers=headers)
        response_data = response.json()
        
        if response.status_code == 200 and response_data.get("code") == 0:
            user_data = response_data["data"]
            print("\n=== 登录用户详细信息 ===")
            print(f"ID: {user_data['id']}")
            print(f"用户名: {user_data['name']}")
            print(f"真实姓名: {user_data['realname']}")
            print(f"手机号: {user_data['cellphone']}")
            print(f"角色: {user_data['role']['name']} (ID: {user_data['role']['id']})")
            print(f"部门: {user_data['department']['name']} (ID: {user_data['department']['id']})")
        else:
            print(f"获取用户信息失败: {response_data.get('message', '未知错误')}")
    except Exception as e:
        print(f"用户信息请求出错: {e}")

def main():
    print("=== 用户登录测试 ===")
    # 显示数据库中的用户
    show_all_users()
    
    # 登录测试
    username = input("\n请输入用户名 (默认: coderwhy): ") or "coderwhy"
    password = input("请输入密码 (默认: 123456): ") or "123456"
    
    token = login(username, password)
    
    if token:
        # 获取并显示用户信息
        get_user_info(token)

if __name__ == "__main__":
    main() 