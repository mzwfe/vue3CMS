# vue3CMS-backend/app/__init__.py
from flask import Flask, jsonify
from .config import get_config
from .extensions import db, cors
import logging

def create_app():
    app = Flask(__name__)

    # 加载配置
    app_config = get_config()
    app.config.from_object(app_config)

    # 初始化扩展
    db.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}}) # 允许所有来源的所有路径跨域请求，生产环境应配置具体的来源

    # 配置日志
    logging.basicConfig(level=logging.DEBUG if app.config['DEBUG'] else logging.INFO)
    app.logger.setLevel(logging.DEBUG if app.config['DEBUG'] else logging.INFO)

    app.logger.info(f"Current database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


    # 注册蓝图 (Blueprints)
    # 确保在导入蓝图之前，相关的依赖（如db）已经初始化
    from .routes.auth import bp as auth_bp
    from .routes.system import bp as system_bp
    from .routes.product_management import bp as product_management_bp
    from .routes.story import bp as story_bp
    from .routes.chart import bp as chart_bp
    # 更多蓝图...

    app.register_blueprint(auth_bp, url_prefix='/api') # 所有auth接口前缀为 /api
    app.register_blueprint(system_bp, url_prefix='/api')
    app.register_blueprint(product_management_bp, url_prefix='/api')
    app.register_blueprint(story_bp, url_prefix='/api')
    app.register_blueprint(chart_bp, url_prefix='/api')

    # 简单的健康检查路由
    @app.route('/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200

    app.logger.info("Flask app created and configured.")
    return app