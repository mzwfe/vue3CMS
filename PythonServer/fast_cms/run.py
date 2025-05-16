# vue3CMS-backend/run.py
from app import create_app
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # 从环境变量或配置中获取调试模式、主机和端口
    # 例如: app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug=app.config.get("DEBUG", True),
            host=app.config.get("HOST", "127.0.0.1"),
            port=app.config.get("PORT", 5000))